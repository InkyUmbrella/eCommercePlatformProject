from django.urls import path
from .views import order_confirm, order_create

urlpatterns = [
    path("confirm/", order_confirm),
    path("", order_create),
]