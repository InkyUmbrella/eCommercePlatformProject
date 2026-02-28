from django.urls import path

from .views import TransactionApiDraftView

urlpatterns = [
    path("transactions/draft", TransactionApiDraftView.as_view(), name="transaction-api-draft"),
]
