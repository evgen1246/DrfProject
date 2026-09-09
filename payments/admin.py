from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_date",
        "course",
        "lesson",
        "amount",
        "payment_method",
        "is_paid",
    )
    list_filter = ("payment_method", "is_paid", "payment_date")
    search_fields = ("user__email",)
    ordering = ("-payment_date",)
    readonly_fields = ("payment_date",)
