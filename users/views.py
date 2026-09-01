from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import (LoginSerializer, PaymentSerializer,
                          UserProfileSerializer, UserRegistrationSerializer,
                          UserUpdateSerializer)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление профиля текущего пользователя с историей платежей"""

    serializer_class = UserProfileSerializer

    def get_object(self) -> User:
        return self.request.user


class RegisterAPIView(CreateAPIView):
    """Регистрация нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "city": user.city,
                "message": "Пользователь успешно зарегистрирован",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """Вход пользователя с выдачей JWT токенов"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone": user.phone,
                    "city": user.city,
                },
            }
        )


class PaymentListView(ListAPIView):
    """Список платежей текущего пользователя с фильтрацией и сортировкой"""

    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related(
            "user", "course", "lesson"
        )


class UserListView(ListCreateAPIView):
    """Список всех пользователей (только для админов)"""

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.none()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление пользователя (только для админов)"""

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.none()
