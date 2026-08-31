from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .apps import UsersConfig
from .views import (
    ProfileRetrieveUpdateAPIView,
    RegisterAPIView,
    LoginAPIView,
    PaymentListView,
    UserListView,
    UserDetailView,
)

app_name = UsersConfig.name

urlpatterns = [
    # Регистрация и вход (без авторизации)
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),

    # JWT токены (без авторизации)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Профиль и платежи (авторизация)
    path("profile/", ProfileRetrieveUpdateAPIView.as_view(), name="profile"),
    path("payments/", PaymentListView.as_view(), name="payments"),

    # CRUD пользователей (админы)
    path("all/", UserListView.as_view(), name="user_list"),
    path("all/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
