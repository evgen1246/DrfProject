from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Payment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "phone", "city", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("phone", "city", "avatar")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_date", "course", "lesson", "amount", "payment_method")
    list_filter = ("payment_method", "payment_date")
    search_fields = ("user__email",)
    ordering = ("-payment_date",)
    readonly_fields = ("payment_date",)