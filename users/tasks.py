from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
@shared_task
def block_inactive_users():
    """Заблокировать обычных пользователей, не заходивших более месяца."""
    one_month_ago = timezone.now() - timedelta(days=30)

    blocked_count = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago,
        is_superuser=False,
        is_staff=False,
    ).update(is_active=False)

    return f"Заблокировано пользователей: {blocked_count}"
