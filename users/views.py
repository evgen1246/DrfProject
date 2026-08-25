from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление профиля текущего пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user


class RegisterAPIView(CreateAPIView):
    """Регистрация нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
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