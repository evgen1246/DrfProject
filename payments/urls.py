from django.urls import path

from .apps import PaymentsConfig
from .views import CreatePaymentView, PaymentCancelView, PaymentSuccessView

app_name = PaymentsConfig.name

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create_payment"),
    path("success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
]
