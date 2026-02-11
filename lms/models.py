from django.db import models


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

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

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

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name_course
