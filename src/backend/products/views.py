from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from common.response import ok
from .models import Category, Product


def _serialize_product(product, request):
    image = ""
    if product.cover_image:
        image = request.build_absolute_uri(product.cover_image.url)
    return {
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock,
        "is_active": product.is_active,
        "cover_image": image,
        "description": product.description,
        "short_description": (product.description or "")[:80],
        "category_id": product.category_id,
        "category_name": product.category.name,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    queryset = Product.objects.filter(is_active=True).select_related("category").order_by("-id")

    keyword = str(request.query_params.get("keyword", "")).strip()
    if keyword:
        queryset = queryset.filter(name__icontains=keyword)

    category_id = request.query_params.get("category_id")
    if category_id:
        queryset = queryset.filter(category_id=category_id)

    ordering = request.query_params.get("ordering")
    if ordering in {"price", "-price", "id", "-id", "created_at", "-created_at"}:
        queryset = queryset.order_by(ordering)

    try:
        page = max(int(request.query_params.get("page", 1) or 1), 1)
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = max(min(int(request.query_params.get("page_size", 20) or 20), 100), 1)
    except (TypeError, ValueError):
        page_size = 20
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    items = queryset[start:end]

    return ok(
        {
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": [_serialize_product(product, request) for product in items],
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def new_products(request):
    queryset = Product.objects.filter(is_active=True).select_related("category").order_by("-created_at")[:8]
    return ok([_serialize_product(product, request) for product in queryset])


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related("category"), id=product_id, is_active=True)
    return ok(_serialize_product(product, request))


@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.order_by("sort_order", "id")
    return ok(
        [
            {
                "id": item.id,
                "name": item.name,
                "parent_id": item.parent_id,
            }
            for item in categories
        ]
    )
