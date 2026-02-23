import smtplib
from calendar import monthrange
from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_about_update_lms(email_list):
    """Отправляет сообщение об обновлении материалов."""

    try:
        send_mail('Обновление курса', 'Материалы курса обновлены', EMAIL_HOST_USER, [email_list], fail_silently=False)
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def check_last_login_by_date():
    """Проверяет пользователей по дате последнего входа по полю last_login. Если пользователь не заходил более месяца, то
    он блокируется - флаг is_active."""
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(zone)
    month = now.month
    year = now.year
    days_count = monthrange(year, month)
    expiration_date = now - timedelta(days=days_count[1])
    user_list = User.objects.filter(last_login__lte=expiration_date, is_active=True)
    user_list.update(is_active=False)