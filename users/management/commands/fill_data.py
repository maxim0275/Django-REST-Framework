import json

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):

    @staticmethod
    def json_read_users():
        # Здесь мы получаем данные из фикстуры с пользователями
        users = []

        with open("users_data.json", 'r') as f:
            data = json.load(f)

        for item in data:
            if item['model'] == 'users.user':
                users.append(item)

        return users

    @staticmethod
    def json_read_courses():
        # Здесь мы получаем данные из фикстуры с курсами
        courses = []

        with open("lms_data.json", 'r') as f:
            data = json.load(f)

        for item in data:
            if item['model'] == 'lms.course':
                courses.append(item)

        return courses

    @staticmethod
    def json_read_lessons():
        # Здесь мы получаем данные из фикстуры с уроками
        lessons = []

        with open("lms_data.json", 'r') as f:
            data = json.load(f)

        for item in data:
            if item['model'] == 'lms.lesson':
                lessons.append(item)

        return lessons

    @staticmethod
    def json_read_payments():
        # Здесь мы получаем данные из фикстуры с платежами
        payments = []

        with open("users_data.json", 'r') as f:
            data = json.load(f)

        for item in data:
            if item['model'] == 'users.payments':
                payments.append(item)

        return payments

    def handle(self, *args, **options):
        # Удалить пользователей
        User.objects.all().delete()
        # Удалить  уроки
        Lesson.objects.all().delete()
        # Удалить курсы
        Course.objects.all().delete()
        # Удалить платежи
        Payments.objects.all().delete()

        # Списки для хранения объектов
        user_for_create = []
        course_for_create = []
        lesson_for_create = []
        payments_for_create = []

        # Обходим все значения пользователей из фикстуры для получения информации об одном объекте
        for user in Command.json_read_users():
            user_for_create.append(
                User(id=user['pk'],
                     password=user['fields']['password'],
                     email=user['fields']['email'],
                     phone=user['fields']['phone'],
                     city=user['fields']['city'],
                     avatar=user['fields']['avatar'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        User.objects.bulk_create(user_for_create)

        # Обходим все значения курсов из фикстуры для получения информации об одном объекте
        for course in Command.json_read_courses():
            course_for_create.append(
                Course(id=course['pk'],
                       name_course=course['fields']['name_course'],
                       preview=course['fields']['preview'],
                       description=course['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Course.objects.bulk_create(course_for_create)

        # Обходим все значения уроков из фикстуры для получения информации об одном объекте
        for lesson in Command.json_read_lessons():
            lesson_for_create.append(
                Lesson(id=lesson['pk'],
                       name_lesson=lesson['fields']['name_lesson'],
                       course=Course.objects.get(pk=lesson['fields']['course']),
                       description=lesson['fields']['description'],
                       preview=lesson['fields']['preview'],
                       video_link=lesson['fields']['video_link'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Lesson.objects.bulk_create(lesson_for_create)

        # Обходим все значения платежей из фикстуры для получения информации об одном объекте
        for payment in Command.json_read_payments():
            lesson_paid = Lesson.objects.filter(pk=payment['fields']['lesson_paid']).first()
            course_paid = Course.objects.filter(pk=payment['fields']['course_paid']).first()
            payments_for_create.append(
                Payments(id=payment['pk'],
                         user_payer=User.objects.get(pk=payment['fields']['user_payer']),
                         date=payment['fields']['date'],
                         course_paid=course_paid,
                         lesson_paid=lesson_paid,
                         payment_amount=payment['fields']['payment_amount'],
                         payment_method=payment['fields']['payment_method'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Payments.objects.bulk_create(payments_for_create)
