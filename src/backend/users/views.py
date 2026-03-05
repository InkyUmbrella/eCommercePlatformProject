from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from common.response import ok, fail
from .models import Address


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "on")


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "").strip()

    if not username or not password:
        return fail("username/password 必填", http_status=400)
    if User.objects.filter(username=username).exists():
        return fail("用户名已存在", http_status=400)

    user = User.objects.create_user(username=username, password=password)
    return ok({"id": user.id, "username": user.username}, "注册成功")


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "").strip()

    user = authenticate(username=username, password=password)
    if not user:
        return fail("用户名或密码错误", http_status=401)

    refresh = RefreshToken.for_user(user)
    return ok({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }, "登录成功")


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    token = request.data.get("refresh", "").strip()
    if not token:
        return fail("refresh 必填", http_status=400)

    try:
        refresh = RefreshToken(token)
        return ok({"access": str(refresh.access_token)}, "刷新成功")
    except Exception:
        return fail("refresh 无效", http_status=401)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return ok({
        "id": request.user.id,
        "username": request.user.username,
    })


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def addresses(request):
    user = request.user

    if request.method == "GET":
        qs = user.addresses.all().order_by("-is_default", "-id")
        data = [
            {
                "id": a.id,
                "name": a.name,
                "address": a.address,
                "phone_number": a.phone_number,
                "is_default": a.is_default,
            }
            for a in qs
        ]
        return ok(data)

    name = str(request.data.get("name", "")).strip()
    address_text = str(request.data.get("address", "")).strip()
    phone_number = str(request.data.get("phone_number", "")).strip()
    is_default = _to_bool(request.data.get("is_default", False))

    if not name or not address_text or not phone_number:
        return fail("name/address/phone_number 必填", http_status=400)

    with transaction.atomic():
        has_default = user.addresses.filter(is_default=True).exists()
        final_default = is_default or (not has_default)

        if final_default:
            user.addresses.update(is_default=False)

        a = Address.objects.create(
            user=user,
            name=name,
            address=address_text,
            phone_number=phone_number,
            is_default=final_default,
        )

    return ok({
        "id": a.id,
        "name": a.name,
        "address": a.address,
        "phone_number": a.phone_number,
        "is_default": a.is_default,
    }, "创建成功")


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def address_detail(request, address_id):
    a = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == "DELETE":
        a.delete()
        return ok(message="删除成功")

    name = request.data.get("name", a.name)
    address_text = request.data.get("address", a.address)
    phone_number = request.data.get("phone_number", a.phone_number)
    is_default_value = request.data.get("is_default", None)

    with transaction.atomic():
        a.name = str(name).strip()
        a.address = str(address_text).strip()
        a.phone_number = str(phone_number).strip()

        if is_default_value is not None and _to_bool(is_default_value):
            request.user.addresses.update(is_default=False)
            a.is_default = True

        a.save()

    return ok({
        "id": a.id,
        "name": a.name,
        "address": a.address,
        "phone_number": a.phone_number,
        "is_default": a.is_default,
    }, "更新成功")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_default_address(request, address_id):
    a = get_object_or_404(Address, id=address_id, user=request.user)

    with transaction.atomic():
        request.user.addresses.update(is_default=False)
        a.is_default = True
        a.save(update_fields=["is_default"])

    return ok({"id": a.id, "is_default": True}, "设置默认成功")
