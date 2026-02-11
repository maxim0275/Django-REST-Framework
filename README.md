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

