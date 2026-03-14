import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from common.response import fail, ok
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
    image = ""
    if order_item.product.cover_image:
        image = order_item.product.cover_image.url
    return {
        "id": order_item.id,
        "product_id": order_item.product_id,
        "product_name": order_item.product.name,
        "title": order_item.product.name,
        "category_name": order_item.product.category.name if order_item.product.category_id else "",
        "image": image,
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
        "aftersale_used": order.aftersale_used,
        "express_company": order.express_company,
        "express_no": order.express_no,
        "shipping_remark": order.shipping_remark,
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
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
        "id": order.id,
        "order_id": order.id,
        "order_no": f"ORD{order.id:08d}",
        "status": order.status,
        "aftersale_used": order.aftersale_used,
        "address": _serialize_address(order.address),
        "express_company": order.express_company,
        "express_no": order.express_no,
        "shipping_remark": order.shipping_remark,
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
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
            .prefetch_related("order_items__product__category")
            .order_by("-id")
        )
        status = str(request.query_params.get("status", "")).strip()
        if status:
            orders = orders.filter(status=status)

        search = str(request.query_params.get("search", "")).strip()
        if search:
            query = Q(order_items__product__name__icontains=search)
            if search.isdigit():
                query = query | Q(id=int(search))
            orders = orders.filter(query).distinct()

        try:
            page = max(int(request.query_params.get("page", 1) or 1), 1)
        except (TypeError, ValueError):
            page = 1
        try:
            page_size = max(min(int(request.query_params.get("page_size", 10) or 10), 100), 1)
        except (TypeError, ValueError):
            page_size = 10

        total = orders.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_orders = orders[start:end]
        return ok(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": [_serialize_order(order, include_items=True) for order in page_orders],
            }
        )

    return _create_order(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("address").prefetch_related("order_items__product__category"),
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


def _create_order(request):
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
def order_create(request):
    return _create_order(request)


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
def order_ship(request, order_id):
    if not request.user.is_staff:
        return fail("forbidden", http_status=403)

    order = get_object_or_404(Order, id=order_id)
    if order.status != "pending_shipment":
        return fail("only pending_shipment can be shipped", http_status=400)

    express_company = str(request.data.get("express_company", "")).strip()
    express_no = str(request.data.get("express_no", "")).strip()
    shipping_remark = str(request.data.get("shipping_remark", "")).strip()
    if not express_company or not express_no or not shipping_remark:
        return fail("express_company/express_no/shipping_remark are required", http_status=400)

    status_before = order.status
    order.express_company = express_company
    order.express_no = express_no
    order.shipping_remark = shipping_remark
    order.shipped_at = timezone.now()
    order.change_status("pending_receipt")
    order.save(update_fields=["status", "express_company", "express_no", "shipping_remark", "shipped_at", "updated_at"])
    logger.info("order shipped staff=%s order=%s", request.user.id, order.id)
    return ok(_serialize_order_status(order, status_before), "order shipped")


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
    if order.aftersale_used:
        return fail("refund already used", http_status=400)

    status_before = order.status
    order.aftersale_used = True
    order.save(update_fields=["aftersale_used"])
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_logistics(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    timeline = [{"text": "订单已提交", "time": order.created_at.isoformat()}] + (
        [{"text": "商家已发货", "time": order.shipped_at.isoformat()}]
        if order.shipped_at
        else []
    )
    return ok(
        {
            "order_id": order.id,
            "company": order.express_company or "待发货",
            "tracking_no": order.express_no or "",
            "express_company": order.express_company or "",
            "express_no": order.express_no or "",
            "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
            "timeline": timeline,
            "traces": timeline,
        }
    )
