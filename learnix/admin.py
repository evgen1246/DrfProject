from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    list_display_links = ("id", "title")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "created_at")
    list_display_links = ("id", "title")
    list_filter = ("course",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)
