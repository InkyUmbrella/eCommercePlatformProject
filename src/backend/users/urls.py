from django.urls import path
from .views import (
    register,
    login,
    me,
    refresh_token,
    addresses,
    address_detail,
    set_default_address,
)

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("refresh/", refresh_token),
    path("me/", me),
    path("addresses/", addresses),
    path("addresses/<int:address_id>/", address_detail),
    path("addresses/<int:address_id>/set-default/", set_default_address),
]
