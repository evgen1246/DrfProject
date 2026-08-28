from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с количеством уроков"""

    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "created_at", "updated_at"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""

    class Meta:
        model = Course
        fields = "__all__"
