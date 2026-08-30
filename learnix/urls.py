from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import LearnixConfig
from .views import (CourseViewSet, LessonListCreateView,
                    LessonRetrieveUpdateDeleteView)

app_name = LearnixConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    # Уроки
    path("lessons/", LessonListCreateView.as_view(), name="lesson_list_create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDeleteView.as_view(),
        name="lesson_detail",
    ),
]
