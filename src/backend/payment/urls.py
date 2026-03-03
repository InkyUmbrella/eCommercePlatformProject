from django.urls import path
from .views import pay_order

urlpatterns = [
    path("orders/<int:order_id>/pay/", pay_order),
]