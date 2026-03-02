from rest_framework.decorators import api_view
from common.response import ok, fail


@api_view(["POST"])
def order_confirm(request):
    address_id = request.data.get("address_id")
    note = request.data.get("note", "")

    if not address_id:
        return fail("address_id 必填", http_status=400)

    return ok({
        "address_id": address_id,
        "note": note,
        "items_amount": "99.00",
        "shipping_fee": "0.00",
        "pay_amount": "99.00",
    })


@api_view(["POST"])
def order_create(request):
    address_id = request.data.get("address_id")
    if not address_id:
        return fail("address_id 必填", http_status=400)

    return ok({
        "order_id": 10001,
        "order_no": "ORD202603010001",
        "status": "PENDING_PAY",
    }, "下单成功")