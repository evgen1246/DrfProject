from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from learnix.models import Course, Lesson, Subscription

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
            video_url="https://youtube.com/watch",
            course=self.course,
            owner=self.owner,
        )

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_list_create")
        data = {
            "title": "Новый урок",
            "description": "Описание",
            "video_url": "https://youtube.com/watch",
            "course": self.course.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_other_user_cannot_create_lesson_in_foreign_course(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("learnix:lesson_list_create")
        data = {
            "title": "Чужой урок",
            "description": "Описание",
            "video_url": "https://youtube.com/watch",
            "course": self.course.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_with_invalid_url(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_list_create")
        data = {
            "title": "Плохой урок",
            "description": "Описание",
            "video_url": "https://rutube.ru/video/abc",
            "course": self.course.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_sees_only_own_lessons(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_other_user_does_not_see_foreign_lessons(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("learnix:lesson_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_moderator_sees_all_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("learnix:lesson_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_owner_can_update_own_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.patch(url, {"title": "Обновлённый урок"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Обновлённый урок")

    def test_moderator_can_update_foreign_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.patch(url, {"title": "Изменено"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.patch(url, {"title": "Взлом"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_own_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_other_user_cannot_delete_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("learnix:lesson_detail", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    """Тесты подписки"""

    def setUp(self):
        self.user = User.objects.create_user(email="user@test.ru", password="test12345")
        self.other_user = User.objects.create_user(
            email="other@test.ru", password="test12345"
        )

        self.course = Course.objects.create(
            title="Python", description="Курс", owner=self.other_user
        )

    def test_user_can_subscribe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("learnix:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(response.data["is_subscribed"])

    def test_user_can_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("learnix:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(response.data["is_subscribed"])

    def test_user_can_list_subscriptions(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("learnix:subscriptions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_cannot_subscribe(self):
        url = reverse("learnix:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_without_course_id(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("learnix:subscriptions")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
