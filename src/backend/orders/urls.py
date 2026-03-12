from django.urls import path
from .views import (
    order_confirm,
    order_create,
    order_pay,
    order_cancel,
    order_confirm_receive,
    order_refund,
    order_refund_complete,
)

urlpatterns = [
    path("confirm/", order_confirm),
    path("", order_create),
    path("<int:order_id>/pay/", order_pay),
    path("<int:order_id>/cancel/", order_cancel),
    path("<int:order_id>/confirm-receive/", order_confirm_receive),
    path("<int:order_id>/refund/", order_refund),
    path("<int:order_id>/refund-complete/", order_refund_complete),
]
