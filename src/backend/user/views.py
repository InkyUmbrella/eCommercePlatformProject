from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from ..common.response import ok, fail


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