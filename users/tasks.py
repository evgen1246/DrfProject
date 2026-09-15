from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def block_inactive_users():
    """Блокирует пользователей, которые не заходили более месяца.Устанавливает is_active = False."""

    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago,
        is_superuser=False,
        is_staff=False,
    )

    blocked_count = 0

    for user in inactive_users:
        user.is_active = False
        user.save(update_fields=["is_active"])
        blocked_count += 1

    return f"Заблокировано пользователей: {blocked_count}"
