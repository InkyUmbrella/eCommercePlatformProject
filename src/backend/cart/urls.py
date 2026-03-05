from django.urls import path
from .views import cart_list, cart_add_item, cart_update_item, cart_select_all

urlpatterns = [
    path("", cart_list),
    path("items/", cart_add_item),
    path("items/<int:item_id>/", cart_update_item),
    path("select-all/", cart_select_all),
]
