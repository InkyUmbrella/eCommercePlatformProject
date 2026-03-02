from rest_framework.decorators import api_view
from common.response import ok


@api_view(["POST"])
def pay_order(request, order_id):
    # Day1 草案：模拟支付成功
    return ok({
        "order_id": order_id,
        "status_before": "PENDING_PAY",
        "status_after": "PENDING_SHIP",
    }, "支付成功")