from django.urls import path

from .views import banners


urlpatterns = [
    path("banners/", banners),
]
