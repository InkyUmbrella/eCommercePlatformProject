from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from common.response import ok, fail
from orders.models import Order, OrderItem
from users.models import Address


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


def _selected_cart_items(user):
    return list(
        CartItem.objects.filter(user=user, selected=True)
        .select_related("product")
        .order_by("-id")
    )


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

    return ok({
        "default_address": _serialize_address(default_address) if default_address else None,
        "addresses": [_serialize_address(a) for a in addresses],
        "items": [_serialize_confirm_item(item) for item in selected_items],
        "items_amount": str(items_amount),
        "shipping_fee": str(shipping_fee),
        "pay_amount": str(pay_amount),
    })


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

    with transaction.atomic():
        for item in selected_items:
            product = item.product
            product.refresh_from_db(fields=["stock", "is_active"])
            if not product.is_active:
                return fail("product is inactive", http_status=400)
            if item.quantity > product.stock:
                return fail("insufficient stock", http_status=400)

        order = Order.objects.create(
            user=user,
            address=address,
            status="pending_payment",
        )

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

    shipping_fee = Decimal("0.00")
    pay_amount = items_amount + shipping_fee

    return ok({
        "order_id": order.id,
        "order_no": f"ORD{order.id:08d}",
        "status": order.status,
        "items_amount": str(items_amount),
        "shipping_fee": str(shipping_fee),
        "pay_amount": str(pay_amount),
    }, "order created")
