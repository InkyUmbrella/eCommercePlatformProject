from django.urls import path

from .views import banners, hot_recommends


urlpatterns = [
    path("banners/", banners),
    path("hot-recommends/", hot_recommends),
]
