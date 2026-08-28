from django_filters import rest_framework as filters

from .models import Payment


class PaymentFilter(filters.FilterSet):
    """Фильтр для платежей"""

    course = filters.NumberFilter(field_name="course", lookup_expr="exact")
    lesson = filters.NumberFilter(field_name="lesson", lookup_expr="exact")
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    date_from = filters.DateTimeFilter(field_name="payment_date", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="payment_date", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "date_from", "date_to"]
