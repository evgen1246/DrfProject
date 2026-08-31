from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Payment, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    user_email = serializers.CharField(source="user.email", read_only=True)
    course_title = serializers.CharField(
        source="course.title", read_only=True, allow_null=True
    )
    lesson_title = serializers.CharField(
        source="lesson.title", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "payment_date",
            "course",
            "course_title",
            "lesson",
            "lesson_title",
            "amount",
            "payment_method",
        ]
        read_only_fields = ["id", "user", "user_email", "payment_date"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с историей платежей"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments")
        read_only_fields = ("id", "email", "payments")


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа (JWT)"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверный email или пароль")


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления пользователя (админ/менеджер)"""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "is_active", "is_staff")
        read_only_fields = ("id", "email")
