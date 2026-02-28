from django.views import View

from common.response import api_success


class TransactionApiDraftView(View):
    """交易域 API 草案（Day1 版本）。"""

    def get(self, request):
        draft = {
            "module": "transaction-core",
            "version": "v1",
            "apis": [
                {
                    "name": "购物车列表",
                    "method": "GET",
                    "path": "/api/v1/cart/items",
                    "desc": "查询当前用户购物车商品",
                },
                {
                    "name": "加入购物车",
                    "method": "POST",
                    "path": "/api/v1/cart/items",
                    "desc": "添加 SKU 到购物车",
                },
                {
                    "name": "更新购物车数量",
                    "method": "PATCH",
                    "path": "/api/v1/cart/items/{item_id}",
                    "desc": "修改购物车商品数量",
                },
                {
                    "name": "确认订单",
                    "method": "POST",
                    "path": "/api/v1/orders/preview",
                    "desc": "根据购物车与地址生成订单预览",
                },
                {
                    "name": "创建订单",
                    "method": "POST",
                    "path": "/api/v1/orders",
                    "desc": "提交订单并生成待支付订单",
                },
                {
                    "name": "模拟支付",
                    "method": "POST",
                    "path": "/api/v1/orders/{order_no}/pay",
                    "desc": "模拟支付并推进订单状态",
                },
            ],
        }
        return api_success(data=draft, message="transaction api draft")
