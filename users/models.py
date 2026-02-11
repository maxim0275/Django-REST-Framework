from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Lessons:
    pass


class Payments(models.Model):
    METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод"),
    ]

    user_payer = models.ForeignKey(
        User,
        verbose_name="Плательщик",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.DateField(auto_now=True, verbose_name="дата платежа")
    course_paid = models.ForeignKey(
        Course,
        related_name="paid_course",
        verbose_name="оплаченный курс",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    lesson_paid = models.ForeignKey(
        Lesson,
        related_name="paid_lesson",
        verbose_name="оплаченный урок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    payment_amount = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты"
    )
    payment_method = models.CharField(max_length=200, choices=METHOD_CHOICES)
    session_id_course = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="id сессии"
    )
    link_course = models.URLField(
        max_length=400, null=True, blank=True, verbose_name="ссылка на оплату"
    )
    session_id_lesson = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="id сессии"
    )
    link_pay = models.URLField(
        max_length=400, null=True, blank=True, verbose_name="ссылка на оплату"
    )

    @property
    def __str__(self):
        return f"{self.user_payer.email} — {self.payment_amount} ₽ — {self.date}"