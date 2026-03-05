from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from common.response import ok, fail
from products.models import Product


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _serialize_item(item):
    product = item.product
    return {
        "id": item.id,
        "product_id": product.id,
        "title": product.name,
        "price": str(product.price),
        "quantity": item.quantity,
        "selected": item.selected,
        "subtotal": str(product.price * item.quantity),
        "stock": product.stock,
        "is_active": product.is_active,
    }


def _build_cart_payload(user):
    items = (
        CartItem.objects
        .filter(user=user)
        .select_related("product")
        .order_by("-id")
    )

    total_amount = Decimal("0.00")
    selected_count = 0
    serialized_items = []

    for item in items:
        serialized_items.append(_serialize_item(item))
        if item.selected:
            total_amount += item.product.price * item.quantity
            selected_count += 1

    return {
        "items": serialized_items,
        "total_amount": str(total_amount),
        "selected_count": selected_count,
        "item_count": len(serialized_items),
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_list(request):
    return ok(_build_cart_payload(request.user))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_add_item(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    if not product_id:
        return fail("product_id is required", http_status=400)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return fail("quantity must be an integer", http_status=400)

    if quantity <= 0:
        return fail("quantity must be greater than 0", http_status=400)

    product = get_object_or_404(Product, id=product_id)
    if not product.is_active:
        return fail("product is inactive", http_status=400)

    item = CartItem.objects.filter(user=request.user, product=product).first()
    new_quantity = quantity if item is None else item.quantity + quantity

    if new_quantity > product.stock:
        return fail("insufficient stock", http_status=400)

    if item is None:
        item = CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
        )
    else:
        item.quantity = new_quantity
        item.save(update_fields=["quantity"])

    item.refresh_from_db()
    return ok({"item": _serialize_item(item)}, "item added")


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_update_item(request, item_id):
    item = get_object_or_404(
        CartItem.objects.select_related("product"),
        id=item_id,
        user=request.user,
    )

    if request.method == "DELETE":
        item.delete()
        return ok(message="item deleted")

    quantity = request.data.get("quantity")
    selected = request.data.get("selected")

    if quantity is None and selected is None:
        return fail("provide quantity or selected", http_status=400)

    update_fields = []

    if quantity is not None:
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return fail("quantity must be an integer", http_status=400)

        if quantity <= 0:
            return fail("quantity must be greater than 0", http_status=400)

        if quantity > item.product.stock:
            return fail("insufficient stock", http_status=400)

        item.quantity = quantity
        update_fields.append("quantity")

    if selected is not None:
        item.selected = _to_bool(selected)
        update_fields.append("selected")

    if update_fields:
        item.save(update_fields=update_fields)

    item.refresh_from_db()
    return ok({"item": _serialize_item(item)}, "item updated")


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def cart_select_all(request):
    selected = request.data.get("selected")
    if selected is None:
        return fail("selected is required", http_status=400)

    CartItem.objects.filter(user=request.user).update(selected=_to_bool(selected))
    return ok(_build_cart_payload(request.user), "select all updated")
