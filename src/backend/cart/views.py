from rest_framework.decorators import api_view
from common.response import ok, fail


@api_view(["GET"])
def cart_list(request):
    # Day1 草案：先返回 mock
    return ok({
        "items": [
            {"id": 1, "product_id": 101, "title": "示例商品", "price": "99.00", "quantity": 1, "selected": True}
        ],
        "total_amount": "99.00"
    })


@api_view(["POST"])
def cart_add_item(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    if not product_id:
        return fail("product_id 必填", http_status=400)
    if int(quantity) <= 0:
        return fail("quantity 必须大于 0", http_status=400)

    return ok({"item_id": 2}, "加入购物车成功")


@api_view(["PATCH"])
def cart_update_item(request, item_id):
    quantity = request.data.get("quantity")
    selected = request.data.get("selected")

    if quantity is None and selected is None:
        return fail("至少传 quantity 或 selected", http_status=400)

    return ok({"item_id": item_id}, "更新成功")