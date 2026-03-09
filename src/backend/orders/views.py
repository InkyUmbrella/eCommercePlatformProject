from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.utils import timezone

from cart.models import CartItem
from common.response import ok, fail
from orders.models import Order, OrderItem
from users.models import Address


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


def _selected_cart_items(user):
    return list(
        CartItem.objects.filter(user=user, selected=True)
        .select_related("product")
        .order_by("-id")
    )

# ===== 新增：序列化订单详情 =====
def _serialize_order(order):
    """序列化订单信息"""
    items = order.order_items.all()
    address = order.address
    
    return {
        "id": order.id,
        "order_no": f"ORD{order.id:08d}",
        "status": order.status,
        "status_display": order.get_status_display(),
        "created_at": order.created_at,
        "address": {
            "name": address.name,
            "phone": address.phone_number,
            "address": address.address,
        },
        "items": [
            {
                "product_id": item.product.id,
                "title": item.product.name,
                "price": str(item.price),
                "quantity": item.quantity,
                "subtotal": str(item.price * item.quantity),
                "image": item.product.cover_image.url if item.product.cover_image else None,
            }
            for item in items
        ],
        "items_amount": str(sum(item.price * item.quantity for item in items)),
        "shipping_fee": "0.00",
        "pay_amount": str(sum(item.price * item.quantity for item in items)),
        # ===== 新增：发货信息 =====
        "shipping_info": {
            "company": order.get_shipping_company_display() if order.shipping_company else None,
            "code": order.shipping_code,
            "time": order.shipping_time,
            "remark": order.shipping_remark,
        } if order.shipping_time else None
    }


def _serialize_order_status(order, status_before):
    return {
        "order_id": order.id,
        "status_before": status_before,
        "status_after": order.status,
    }


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

    try:
        with transaction.atomic():
            for item in selected_items:
                product = item.product
                product.refresh_from_db(fields=["stock", "is_active"])
                if not product.is_active:
                    raise OrderCreateError("product is inactive")
                if item.quantity > product.stock:
                    raise OrderCreateError("insufficient stock")

            order = Order.objects.create(
                user=user,
                address=address,
                status='pending_payment',
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
    except OrderCreateError as exc:
        return fail(str(exc), http_status=400)

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

# ===== 新增：订单详情接口 =====
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """获取订单详情"""
    user = request.user
    
    # 普通用户只能看自己的订单，管理员可以看所有
    if user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=user)
    
    return ok(_serialize_order(order))


# ===== 新增：发货接口（仅管理员）=====
@api_view(["POST"])
@permission_classes([IsAdminUser])  # 只有管理员可以发货
def order_ship(request, order_id):
    """订单发货"""
    order = get_object_or_404(Order, id=order_id)
    
    # 检查订单状态
    if order.status != 'pending_shipment':
        return fail(f"订单状态错误，当前状态：{order.get_status_display()}，不能发货", http_status=400)
    
    # 获取请求参数
    shipping_company = request.data.get("shipping_company")
    shipping_code = request.data.get("shipping_code")
    shipping_remark = request.data.get("shipping_remark", "")
    
    if not shipping_company:
        return fail("请选择物流公司", http_status=400)
    if not shipping_code:
        return fail("请输入物流单号", http_status=400)
    
    try:
        # 调用 Order 模型的 ship 方法
        order.ship(shipping_company, shipping_code, shipping_remark)
        
        return ok({
            "order_id": order.id,
            "status": order.status,
            "status_display": order.get_status_display(),
            "shipping_info": {
                "company": order.get_shipping_company_display(),
                "code": order.shipping_code,
                "time": order.shipping_time,
                "remark": order.shipping_remark,
            }
        }, "发货成功")
    except ValueError as e:
        return fail(str(e), http_status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_pay(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'pending_payment':
        return fail("only pending_payment can be paid", http_status=400)

    status_before = order.status
    order.change_status('pending_shipment')
    return ok(_serialize_order_status(order, status_before), "order has paid")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cancellable_statuses = {
        'pending_payment',
        'pending_shipment',
        'refund_processing',
    }
    if order.status not in cancellable_statuses:
        return fail("current status cannot be cancelled", http_status=400)

    status_before = order.status
    order.change_status('cancelled')
    return ok(_serialize_order_status(order, status_before), "order cancelled")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_confirm_receive(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'pending_receipt':
        return fail("only pending_receipt can be confirmed", http_status=400)

    status_before = order.status
    order.change_status('completed')
    return ok(_serialize_order_status(order, status_before), "order completed")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_refund(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    refundable_statuses = {
        'pending_receipt',
        'completed',
    }
    if order.status not in refundable_statuses:
        return fail("current status cannot start refund", http_status=400)

    status_before = order.status
    order.change_status('refund_processing')
    return ok(_serialize_order_status(order, status_before), "refund processing started")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_refund_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'refund_processing':
        return fail("only refund_processing can be completed", http_status=400)

    status_before = order.status
    order.change_status('completed')
    return ok(_serialize_order_status(order, status_before), "refund processing completed")
