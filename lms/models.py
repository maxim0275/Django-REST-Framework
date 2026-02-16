from django.db import models

from config import settings


class Course(models.Model):
    name_course = models.CharField(max_length=200, blank=False, null=False)
    preview = models.ImageField(
        upload_to="users/previews/",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    description = models.TextField(blank=True,
                                   null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец курса", help_text="Укажите владельца курса")


    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name_course"]

    def __str__(self):
        return self.name_course


class Lesson(models.Model):
    name_lesson = models.CharField(max_length=200, blank=False, null=False)
    preview = models.ImageField(
        upload_to="users/previews/",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    description = models.TextField(blank=True,
                                   null=True)
    video_link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name="Владелец урока",
                              help_text="Укажите владельца урока")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name_course
