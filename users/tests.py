from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from learnix.models import Course, Lesson

from .models import Payment

User = get_user_model()


class PaymentTests(TestCase):
    """Тесты для платежей"""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            id=1, email="user1@mail.ru", password="test12345"
        )
        self.user2 = User.objects.create_user(
            id=2, email="user2@mail.ru", password="test12345"
        )

        self.course1 = Course.objects.create(
            id=4, title="Python для начинающих", description="Полный курс по Python"
        )
        self.course2 = Course.objects.create(
            id=2, title="Java для начинающих", description="Полный курс по Java"
        )

        self.lesson = Lesson.objects.create(
            id=1,
            title="Установка Python",
            description="Как установить Python",
            video_url="https://www.youtube.com/watch?v=example",
            course=self.course1,
        )

        self.payment1 = Payment.objects.create(
            id=1,
            user=self.user1,
            course=self.course1,
            amount=1111.00,
            payment_method="transfer",
        )
        self.payment2 = Payment.objects.create(
            id=2,
            user=self.user1,
            lesson=self.lesson,
            amount=1000.00,
            payment_method="cash",
        )
        self.payment3 = Payment.objects.create(
            id=3,
            user=self.user2,
            course=self.course2,
            amount=999.00,
            payment_method="transfer",
        )

    def test_user_see_only_own_payments(self):
        """Тест: пользователь видит только свои платежи"""
        self.client.force_authenticate(user=self.user1)

        url = reverse("users:payments")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        for payment in response.data:
            self.assertEqual(payment["user"], self.user1.id)
