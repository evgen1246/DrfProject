from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя (только чтение и обновление)"""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar")
        read_only_fields = ("id", "email")