from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from learnix.models import Course, Lesson

User = get_user_model()


class LessonCRUDTestCase(APITestCase):
    """Тесты CRUD для уроков"""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.ru", password="test12345"
        )
        self.other_user = User.objects.create_user(
            email="other@test.ru", password="test12345"
        )
        self.moderator = User.objects.create_user(
            email="moderator@test.ru", password="test12345"
        )

        moderators_group, _ = Group.objects.get_or_create(name="Модераторы")
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            title="Python для начинающих",
            description="Полный курс по Python",
            owner=self.owner,
        )

        self.lesson = Lesson.objects.create(
            title="Установка Python",
            description="Как установить Python",
            video_url="https://youtube.com/watch?v=abc123",
            course=self.course,
            owner=self.owner,
        )
    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_list_create")
        data = {
            "title": "Новый урок",
            "description": "Описание",
            "video_url": "https://youtube.com/watch?v=new123",
            "course": self.course.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

