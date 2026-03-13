from django.urls import path

from .views import product_list, product_detail, new_products, category_list


urlpatterns = [
    path("", product_list),
    path("new/", new_products),
    path("<int:product_id>/", product_detail),
    path("categories/", category_list),
]
