from django.urls import path

from .views import support_messages, support_reply

urlpatterns = [
    path("messages/", support_messages),
    path("messages/<int:message_id>/reply/", support_reply),
]
