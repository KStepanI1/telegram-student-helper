from django.db import models
from multiselectfield import MultiSelectField
from django import forms

TYPES = (
    ('lec', 'Лекция'),
    ('prac', 'Практика')
)

LESSON_NUMBERS = (
    ("1", "1-ая пара"),
    ("2", "2-ая пара"),
    ("3", "3-яя пара"),
    ("4", "4-ая пара"),
    ("5", "5-ая пара"),
    ("6", "6-ая пара"),
    ("7", "7-ая пара"),
)

WEEK_PARITIES = (
    ("1", "Нечетная"),
    ("2", "Четная"),
)


class TimeBasedModels(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModels):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID пользователя Telegram")
    name = models.CharField(max_length=100, verbose_name="Имя пользователя", blank=True, null=True)
    username = models.CharField(max_length=100, verbose_name="Username Telegram", blank=True, null=True)

    def __str__(self):
        return f"№{self.id} {self.user_id} - {self.name}"


class Subject(TimeBasedModels):
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return f"№{self.id} - {self.name}"


class ZoomLink(TimeBasedModels):
    class Meta:
        verbose_name = "ZOOM ссылка"
        verbose_name_plural = "ZOOM ссылки"

    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name="Предмет", on_delete=models.SET(0))
    type = MultiSelectField(choices=TYPES, max_choices=2)
    url = models.URLField(verbose_name="Ссылка (optional)", blank=True, null=True)
    code = models.CharField(max_length=100, verbose_name="Код")
    password = models.CharField(max_length=100, verbose_name="Пароль (optional)", blank=True, null=True)

    def __str__(self):
        return f"№{self.id} - {self.subject} ({self.type})"


class Teacher(TimeBasedModels):
    class Meta:
        verbose_name = "Перподаватель"
        verbose_name_plural = "Преподаватели"

    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество (optional)", blank=True, null=True)
    subject = models.ForeignKey(Subject, verbose_name="Предмет", on_delete=models.SET(0))
    type = MultiSelectField(choices=TYPES, max_choices=2, verbose_name="Тип пары")
    email = models.EmailField(verbose_name="Email адрес")

    def __str__(self):
        return f"№{self.id} - {self.first_name} {self.middle_name} ({self.subject} - {self.type})"


class Weekday(TimeBasedModels):
    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, verbose_name="Код", default=1)
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Timetable(TimeBasedModels):
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"

    id = models.AutoField(primary_key=True)
    weekday = models.ForeignKey(Weekday, verbose_name="День недели", on_delete=models.SET(0))
    lesson_number = MultiSelectField(choices=LESSON_NUMBERS, verbose_name="Номер пары")
    subject = models.ForeignKey(Subject, verbose_name="Предмет", on_delete=models.SET(0))
    audience_number = models.CharField(max_length=100, verbose_name="Номер аудитории (optional)", blank=True, null=True)
    type = MultiSelectField(choices=TYPES, max_choices=1, verbose_name="Тип пары")
    week_parity = MultiSelectField(choices=WEEK_PARITIES, verbose_name="Четность недели")

    def __str__(self):
        return f"№{self.id} - {self.weekday} {self.subject} (Пара №{self.lesson_number})"


