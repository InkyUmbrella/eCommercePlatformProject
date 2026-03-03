from django.urls import path
from .views import register, login, me, refresh_token

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("refresh/", refresh_token),
    path("me/", me),
]