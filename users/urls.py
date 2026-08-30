from django.urls import path

from .apps import UsersConfig
from .views import (PaymentListView, ProfileRetrieveUpdateAPIView,
                    RegisterAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("profile/", ProfileRetrieveUpdateAPIView.as_view(), name="profile"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("payments/", PaymentListView.as_view(), name="payments"),
]
