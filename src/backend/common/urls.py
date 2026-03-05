from django.urls import path

from .views import support_messages

urlpatterns = [
    path("messages/", support_messages),
]
