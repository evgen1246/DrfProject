from django.conf import settings
from django.db import models

from learnix.models import Course, Lesson


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("stripe", "Stripe"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        related_name="payments",
        blank=True,
        null=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        related_name="payments",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="stripe",
        verbose_name="Способ оплаты",
    )
    stripe_session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe"
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID PaymentIntent Stripe"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        target = self.course if self.course else self.lesson
        return f"Платеж #{self.id} - {self.user.email} - {target}"
