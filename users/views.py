from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление профиля текущего пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
