import logging
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from common.response import ok, fail
from orders.models import Order, OrderItem
from users.models import Address

logger = logging.getLogger(__name__)


class OrderCreateError(Exception):
    pass


def _serialize_address(address):
    return {
        "id": address.id,
        "name": address.name,
        "address": address.address,
        "phone_number": address.phone_number,
        "is_default": address.is_default,
    }


def _serialize_confirm_item(item):
    product = item.product
    return {
        "cart_item_id": item.id,
        "product_id": product.id,
        "title": product.name,
        "price": str(product.price),
        "quantity": item.quantity,
        "stock": product.stock,
        "subtotal": str(product.price * item.quantity),
    }


def _serialize_order_item(order_item):
    return {
        "id": order_item.id,
        "product_id": order_item.product_id,
        "title": order_item.product.name,
        "price": str(order_item.price),
        "quantity": order_item.quantity,
        "subtotal": str(order_item.price * order_item.quantity),
    }


def _selected_cart_items(user):
    return list(
        CartItem.objects.filter(user=user, selected=True)
        .select_related("product")
        .order_by("-id")
    )


def _serialize_order_status(order, status_before):
    return {
        "order_id": order.id,
        "status_before": status_before,
        "status_after": order.status,
    }


def _calculate_order_amount(order):
    items_amount = sum(
        (item.price * item.quantity for item in order.order_items.all()),
        Decimal("0.00"),
    )
    shipping_fee = Decimal("0.00")
    pay_amount = items_amount + shipping_fee
    return items_amount, shipping_fee, pay_amount


def _serialize_order(order, include_items=False):
    items_amount, shipping_fee, pay_amount = _calculate_order_amount(order)
    payload = {
        "order_no": f"ORD{order.id:08d}",
        "status": order.status,
        "address": _serialize_address(order.address),
        "items_amount": str(items_amount),
        "shipping_fee": str(shipping_fee),
        "pay_amount": str(pay_amount),
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    }
    if include_items:
        payload["items"] = [_serialize_order_item(i) for i in order.order_items.all()]
    return payload


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orders_root(request):
    if request.method == "GET":
        orders = (
            Order.objects.filter(user=request.user)
            .select_related("address")
            .prefetch_related("order_items__product")
            .order_by("-id")
        )
        return ok([_serialize_order(order, include_items=True) for order in orders])

    return order_create(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("address").prefetch_related("order_items__product"),
        id=order_id,
        user=request.user,
    )
    return ok(_serialize_order(order, include_items=True))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_confirm(request):
    user = request.user
    addresses = list(user.addresses.all().order_by("-is_default", "-id"))
    default_address = next((a for a in addresses if a.is_default), None)
    selected_items = _selected_cart_items(user)

    if not selected_items:
        return fail("no selected cart items", http_status=400)

    invalid_item = next(
        (item for item in selected_items if (not item.product.is_active or item.quantity > item.product.stock)),
        None,
    )
    if invalid_item:
        if not invalid_item.product.is_active:
            return fail("product is inactive", http_status=400)
        return fail("insufficient stock", http_status=400)

    items_amount = sum((item.product.price * item.quantity for item in selected_items), Decimal("0.00"))
    shipping_fee = Decimal("0.00")
    pay_amount = items_amount + shipping_fee

    return ok(
        {
            "default_address": _serialize_address(default_address) if default_address else None,
            "addresses": [_serialize_address(a) for a in addresses],
            "items": [_serialize_confirm_item(item) for item in selected_items],
            "items_amount": str(items_amount),
            "shipping_fee": str(shipping_fee),
            "pay_amount": str(pay_amount),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_create(request):
    user = request.user
    address_id = request.data.get("address_id")
    if not address_id:
        return fail("address_id is required", http_status=400)

    address = get_object_or_404(Address, id=address_id, user=user)
    selected_items = _selected_cart_items(user)
    if not selected_items:
        return fail("no selected cart items", http_status=400)

    try:
        with transaction.atomic():
            for item in selected_items:
                product = item.product
                product.refresh_from_db(fields=["stock", "is_active"])
                if not product.is_active:
                    raise OrderCreateError("product is inactive")
                if item.quantity > product.stock:
                    raise OrderCreateError("insufficient stock")

            order = Order.objects.create(user=user, address=address, status="pending_payment")

            order_items = []
            items_amount = Decimal("0.00")
            for item in selected_items:
                product = item.product
                items_amount += product.price * item.quantity
                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price,
                    )
                )
                product.stock = product.stock - item.quantity
                product.save(update_fields=["stock"])

            OrderItem.objects.bulk_create(order_items)
            CartItem.objects.filter(id__in=[item.id for item in selected_items]).delete()

    except OrderCreateError as exc:
        logger.warning("order create failed user=%s reason=%s", user.id, exc)
        return fail(str(exc), http_status=400)

    shipping_fee = Decimal("0.00")
    pay_amount = items_amount + shipping_fee

    logger.info("order created user=%s order=%s", user.id, order.id)
    return ok(
        {
            "order_id": order.id,
            "order_no": f"ORD{order.id:08d}",
            "status": order.status,
            "items_amount": str(items_amount),
            "shipping_fee": str(shipping_fee),
            "pay_amount": str(pay_amount),
        },
        "order created",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_pay(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != "pending_payment":
        return fail("only pending_payment can be paid", http_status=400)

    status_before = order.status
    order.change_status("pending_shipment")
    logger.info("order paid user=%s order=%s", request.user.id, order.id)
    return ok(_serialize_order_status(order, status_before), "order paid")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cancellable_statuses = {
        "pending_payment",
        "pending_shipment",
        "refund_processing",
    }
    if order.status not in cancellable_statuses:
        return fail("current status cannot be cancelled", http_status=400)

    status_before = order.status
    order.change_status("cancelled")
    logger.info("order cancelled user=%s order=%s from=%s", request.user.id, order.id, status_before)
    return ok(_serialize_order_status(order, status_before), "order cancelled")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_confirm_receive(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != "pending_receipt":
        return fail("only pending_receipt can be confirmed", http_status=400)

    status_before = order.status
    order.change_status("completed")
    logger.info("order confirmed user=%s order=%s", request.user.id, order.id)
    return ok(_serialize_order_status(order, status_before), "order completed")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_refund(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    refundable_statuses = {
        "pending_receipt",
        "completed",
    }
    if order.status not in refundable_statuses:
        return fail("current status cannot start refund", http_status=400)

    status_before = order.status
    order.change_status("refund_processing")
    logger.info("order refund started user=%s order=%s", request.user.id, order.id)
    return ok(_serialize_order_status(order, status_before), "refund processing started")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_refund_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != "refund_processing":
        return fail("only refund_processing can be completed", http_status=400)

    status_before = order.status
    order.change_status("completed")
    logger.info("order refund completed user=%s order=%s", request.user.id, order.id)
    return ok(_serialize_order_status(order, status_before), "refund processing completed")
