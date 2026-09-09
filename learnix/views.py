from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator, IsOwner, IsOwnerOrModerator

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с курсами"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        # Модераторы видят все курсы
        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()
        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied("Модераторы не могут создавать курсы")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied("Модераторы не могут удалять курсы")
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить этот курс")
        instance.delete()


class LessonListCreateView(generics.ListCreateAPIView):
    """Список уроков и создание нового урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        # Модераторы видят все уроки
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied("Модераторы не могут создавать уроки")

        course = serializer.validated_data.get("course")
        if course and course.owner != self.request.user:
            raise PermissionDenied("Вы не можете создавать уроки в чужих курсах")
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        course = serializer.validated_data.get("course")
        if course and course.owner != self.request.user:
            if not self.request.user.groups.filter(name="Модераторы").exists():
                raise PermissionDenied("Вы не можете перенести урок в чужой курс")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied("Модераторы не могут удалять уроки")
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить этот урок")
        instance.delete()
