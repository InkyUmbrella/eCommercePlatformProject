from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from common.response import ok
from products.views import _serialize_product

from .models import Banner, HotRecommend


def _serialize_banner(item, request):
    image = request.build_absolute_uri(item.image.url) if item.image else ""
    link = item.link
    if item.product_id:
        link = f"/product-detail/{item.product_id}"
    return {
        "id": item.id,
        "title": item.title,
        "subtitle": item.subtitle,
        "image": image,
        "btn_text": "立即查看",
        "link": link,
        "product_id": item.product_id,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def banners(request):
    queryset = Banner.objects.filter(is_active=True).order_by("sort_order", "-id")
    return ok([_serialize_banner(item, request) for item in queryset])


@api_view(["GET"])
@permission_classes([AllowAny])
def hot_recommends(request):
    queryset = (
        HotRecommend.objects.filter(is_active=True, product__is_active=True)
        .select_related("product__category")
        .order_by("sort_order", "-id")
    )
    payload = []
    for item in queryset:
        product_data = _serialize_product(item.product, request)
        product_data["recommend_title"] = item.title or item.product.name
        payload.append(product_data)
    return ok(payload)
