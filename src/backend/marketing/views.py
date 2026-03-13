from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from common.response import ok
from products.models import Product


@api_view(["GET"])
@permission_classes([AllowAny])
def banners(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")[:3]
    payload = []
    for idx, product in enumerate(products, start=1):
        image = request.build_absolute_uri(product.cover_image.url) if product.cover_image else ""
        payload.append(
            {
                "id": idx,
                "title": product.name,
                "subtitle": (product.description or "")[:32],
                "image": image,
                "btn_text": "立即查看",
                "link": f"/product-detail/{product.id}",
            }
        )
    return ok(payload)
