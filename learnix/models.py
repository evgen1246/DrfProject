from django.db import models


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(
        max_length=255, verbose_name="Название", help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(
        max_length=255, verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео (YouTube, Vimeo и т.д.)",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lessons",
        help_text="Выберите курс, к которому относится урок",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
