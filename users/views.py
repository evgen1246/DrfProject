from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from .filters import PaymentFilter
from .models import User, Payment
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление профиля текущего пользователя с историей платежей"""

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

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
                "message": "Пользователь успешно зарегистрирован"
            },
            status=status.HTTP_201_CREATED
        )


class PaymentListView(ListAPIView):
    """Список платежей текущего пользователя с фильтрацией и сортировкой"""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related("user", "course", "lesson")