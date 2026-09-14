from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Subscription


@shared_task
def send_course_update_email(course_id: int):
    """Отправляет письмо всем подписчикам курса об обновлении."""
    from .models import Course

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return f"Курс с id={course_id} не найден"

    subscriptions = Subscription.objects.filter(course=course).select_related("user")

    if not subscriptions.exists():
        return "Нет подписчиков"

    sent_count = 0
    errors = []

    for subscription in subscriptions:
        user = subscription.user
        try:
            send_mail(
                subject=f"Обновление курса: {course.title}",
                message=f"""
Здравствуйте, {user.email}!

Курс "{course.title}", на который вы подписаны, был обновлён.

Описание курса:
{course.description}

Проверьте новые материалы на сайте.

С уважением,
Команда сервиса
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            sent_count += 1
        except Exception as e:
            errors.append(f"{user.email}: {e}")

    return f"Отправлено писем: {sent_count}, ошибок: {len(errors)}"