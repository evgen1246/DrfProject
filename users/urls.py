from django.urls import path

from .views import (PaymentListView, ProfileRetrieveUpdateAPIView,
                    RegisterAPIView)

app_name = "users"

urlpatterns = [
    path("profile/", ProfileRetrieveUpdateAPIView.as_view(), name="profile"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("payments/", PaymentListView.as_view(), name="payments"),
]
