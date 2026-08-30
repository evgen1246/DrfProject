from django.core.management.base import BaseCommand

from learnix.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создание тестовых платежей"

    def handle(self, *args, **options):
        # Получаем или создаём пользователей
        user1, _ = User.objects.get_or_create(
            email="user1@mail.ru", defaults={"phone": "+7 999 111-22-33"}
        )
        user2, _ = User.objects.get_or_create(
            email="user2@mail.ru", defaults={"phone": "+7 999 444-55-66"}
        )

        course1 = Course.objects.first()
        lesson1 = Lesson.objects.first()

        if not course1 or not lesson1:
            self.stdout.write(self.style.ERROR("Сначала создайте курсы и уроки!"))
            return

        Payment.objects.create(
            user=user1, course=course1, amount=1500.00, payment_method="transfer"
        )

        Payment.objects.create(
            user=user1, lesson=lesson1, amount=500.00, payment_method="cash"
        )

        Payment.objects.create(
            user=user2, course=course1, amount=2000.00, payment_method="transfer"
        )
