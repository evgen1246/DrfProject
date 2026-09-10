from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_only


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    video_url = serializers.URLField(
        validators=[validate_youtube_only],
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "video_url",
            "course",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с количеством уроков и списком уроков"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "created_at",
            "updated_at",
            "is_subscribed",
        ]
        read_only_fields = ["owner"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Возвращает True, если текущий пользователь подписан на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False



class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""

    class Meta:
        model = Subscription
        fields = ["id", "user", "course", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
