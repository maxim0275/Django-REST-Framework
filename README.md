Задание 1

Создан новый Django-проект, подключен DRF в настройках проекта.

Задание 2

Созданы приложения users и lms
Созданы следующие модели
 - "пользователь" в приложении users;
 - "курс" и "урок" в приложении lms

Задание 3

Описаны CRUD для моделей курса и урока
Для реализации CRUD для курса использован Viewsets
Для реализации CRUD для урока  использован Generic-классы

Для работы контроллеров описаны простейшие сериализаторы

-----------------------------------------------------------
30.2 Сериализаторы

**Задание 1**

Для модели курса добавлено в сериализатор поле вывода количества уроков. Поле реализовано с помощью SerializerMethodField()

**Задание 2**

Добавлена новая модель в приложение users
Создан файл с исходными данными (фикстура) и кастомная команда, записывающая данные в таблицы

**Задание 3**

Для сериализатора для модели курса реализовано поле вывода уроков.
Вывод реализован с помощью сериализатора для связанной модели (Lesson).

lesson_in_course = LessonSerializer(source='lesson_set', many=True)
фрагмент вывода:
`[
    {
        "id": 2,
        "lessons_count": 4,
        "lesson_in_course": [
            {
                "id": 2,
                "name_lesson": "Урок 0",
                "preview": null,
                "description": "Начало начал!",
                "video_link": null,
                "course": 2
            },

**Задание 4**

Настроена фильтрация для эндпоинта вывода списка платежей с возможностями:

     - менять порядок сортировки по дате оплаты,

     - фильтровать по курсу или уроку,

     - фильтровать по способу оплаты.

```
class PaymentListView(ListAPIView):
    queryset = Payments.objects.all()
        
    serializer_class = PaymentsSerializer
        
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        
    filterset_fields = ['course_paid', 'lesson_paid', 'payment_method']
        
    search_fields = ['course_paid', 'lesson_paid', 'payment_method']
        
    ordering_fields = ['date']
   ```
__

31 Права доступа в DRF
Задание 1

Настроено в проекте использование JWT-авторизации

Реализованы CRUD для пользователей, в том числе регистрацию пользователей

Настроено так, что доступ к  эндпоинтам update и retrieve предоставлен только авторизованным пользователям

Эндпоинты для авторизации и регистрации доступны для неавторизованных пользователей.

Задание 2

Заведена группа модераторов (фикстура groups.json) 

описаны для нее права работы с любыми уроками и курсами, но без возможности их удалять и создавать новые. 

Заложен функционал проверки в контроллеры.


Задание 3

Описаны права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть, редактировать и удалять только свои курсы и уроки.

-----------------------------------------------------------

**32.1 Валидаторы, пагинация и тесты**

**Задание 1**

Для сохранения уроков и курсов реализована дополнительную проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.

`    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val and 'youtube.com' not in tmp_val:
            raise ValidationError("Нельзя использовать ссылки на сторонние ресурсы.")`

**Задание 2**

Добавлена модель подписки на обновления курса для пользователя.

Реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({"message": message})

Зарегистрирован новый контроллер в url и проверена его работоспособность в Postman.


При выборке данных по курсу пользователю присылается признак подписки текущего пользователя на курс - 
дается информация, подписан пользователь на обновления курса или нет.

    def get_is_subscription(self, course):
        owner = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, user=owner.id)
        if subscription:
            return True
        return False

    lessons_info = LessonSerializer(
        source='lessons',
        many=True,
        read_only=True,
    )

**Задание 3**

Реализована пагинацию для вывода всех уроков и курсов.

Пагинация реализована в отдельном файле paginators.py


**Задание 4**

Написаны тесты, которые проверяют корректность работы CRUD уроков и функционал работы подписки на обновления курса.

`Destroying test database for alias 'default'...

(vsag30-1-py3.13) PS C:\Users\user2\MailingP\VSAG30_1> python manage.py test

Found 13 test(s).

Creating test database for alias 'default'...

System check identified no issues (0 silenced).

.......C:\Users\user2\MailingP\VSAG30_1\.venv\Lib\site-packages\rest_framework\pagination.py:207: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'lms.models.Lesson'> Q
uerySet.

  paginator = self.django_paginator_class(queryset, page_size)
......

Ran 13 tests in 0.642s

OK

Destroying test database for alias 'default'...
`
-----------------------------------------------------------
32.2 Документирование и безопасность

Задание 1

Подключен и настроен вывод документации для проекта. 

Задание 2

Подключена возможность оплаты курсов через https://stripe.com/docs/api.


-----------------------------------------------------------

33 Celery

Настроен проект для работы с Celery. 

    `(vsag30-1-py3.13) PS C:\Users\user2\MailingP\VSAG30_1> celery -A config worker -l info
     
     -------------- celery@MPC02 v5.6.2 (recovery)
    --- ***** -----
    -- ******* ---- Windows-10-10.0.19045-SP0 2026-02-23 13:40:21
    - *** --- * ---
      - ** ---------- [config]
      - ** ---------- .> app:         config:0x2397bce30e0
      - ** ---------- .> transport:   redis://localhost:6379//
      - ** ---------- .> results:     redis://localhost:6379/
      - *** --- * --- .> concurrency: 4 (prefork)
      -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
      --- ***** -----
       -------------- [queues]
                      .> celery           exchange=celery(direct) key=celery
    
    
    [tasks]
      . lms.tasks.check_last_login_by_date
      . lms.tasks.send_about_update_materials
    
    [2026-02-23 13:40:21,876: INFO/MainProcess] Connected to redis://localhost:6379//
    [2026-02-23 13:40:21,899: INFO/MainProcess] mingle: searching for neighbors
    [2026-02-23 13:40:22,969: INFO/MainProcess] mingle: all alone
    [2026-02-23 13:40:23,056: INFO/MainProcess] celery@MPC02 ready.
    [2026-02-23 13:40:23,246: INFO/SpawnPoolWorker-3] child process 11384 calling self.run()
    [2026-02-23 13:40:23,266: INFO/SpawnPoolWorker-1] child process 6828 calling self.run()
    [2026-02-23 13:40:23,302: INFO/SpawnPoolWorker-4] child process 15220 calling self.run()
    [2026-02-23 13:40:23,388: INFO/SpawnPoolWorker-2] child process 17492 calling self.run()`

Настроено приложение на работу с celery-beat для выполнения периодических задач.

`CELERY_BEAT_SCHEDULE = {
    'check_last_login_by_date': {
        'task': 'lms.tasks.check_last_login_by_date',  # Путь к задаче
        'schedule': timedelta(days=1),  # Расписание выполнения задачи (например, каждый день)
    },
}`

Задание 2

Добавлена асинхронная рассылка писем пользователям об обновлении материалов курса.

    def update(self, request, *args, **kwargs):
        """Отправка пользователям, имеющим подписку на курс, информации об обновлении курса."""
        # Список пользователей, подписанных на курс
        email_list = list(Subscription.objects.filter(course=kwargs['pk']).values_list('user__email', flat=True))
        send_about_update_lms.delay(email_list)
        return super().update(request, *args, **kwargs)


Задание 3

С помощью celery-beat реализована фоновая задача, которая проверяет пользователей по дате последнего входа по полю last_login и, если пользователь не заходил более месяца, блокировать его с помощью флага is_active.

РАСПИСАНИЕ

    CELERY_BEAT_SCHEDULE = {
        'check_last_login_by_date': {
            'task': 'lms.tasks.check_last_login_by_date',  # Путь к задаче
            'schedule': timedelta(days=1),  # Расписание выполнения задачи (например, каждый день)
        },
    }

ЗАДАЧА
    def check_last_login_by_date():