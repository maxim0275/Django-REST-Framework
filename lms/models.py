from lms import models
from django.db import models


class Course(models.Model):
    name_course = models.EmailField(unique=True, verbose_name="Курс")
    preview = models.ImageField(
        upload_to="users/previews/",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    description = models.TextField()

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name_course


class Lesson(models.Model):
    name_lesson = models.EmailField(unique=True, verbose_name="Урок")
    preview = models.ImageField(
        upload_to="users/previews/",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    description = models.TextField()
    video_link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name_course
