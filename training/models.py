from django.contrib.auth.models import User
from django.db import models


class Exercise(models.Model):
    """Физическое упражнение"""

    TYPE_CHOICES = [
        ("P", "Сила"),
        ("E", "Выносливость"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=255)
    exercise_type = models.CharField(
        "Тип",
        choices=TYPE_CHOICES,
        default="P",
        max_length=1,
    )
    description = models.TextField("Описание")
    target_muscles = models.TextField("Целевые мышцы", null=True, blank=True)
    mistakes = models.TextField(
        "Основные ошибки выполнения", null=True, blank=True
    )
    icon = models.ImageField(
        "Иконка",
        upload_to="training/img/exercise_icons/",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_1 = models.ImageField(
        "Фото или гифка",
        upload_to="training/img/exercise_photos/",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_2 = models.ImageField(
        "Фото или гифка",
        upload_to="training/img/exercise_photos/",
        max_length=255,
        null=True,
        blank=True,
    )
    effect_areas = models.TextField(
        "Список областей воздействия", null=True, blank=True
    )
    video = models.URLField("Видео", null=True, blank=True)

    def __str__(self):
        return f"Упражнение '{self.name}', автор: {self.author}"

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class Training(models.Model):
    """Тренировка"""

    TYPE_CHOICES = [
        ("P", "Силовая"),
        ("R", "Круговая"),
        ("E", "Выносливость"),
        ("I", "Интервальная"),
    ]

    date = models.DateField("Дата тренировки")
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    training_type = models.CharField(
        "Тип тренировки",
        choices=TYPE_CHOICES,
        max_length=2,
    )
    tiredness_due = models.PositiveSmallIntegerField(
        "Утомление (запланировано)", null=True, blank=True
    )
    tiredness_get = models.PositiveSmallIntegerField(
        "Утомление (получено)", null=True, blank=True
    )
    comment = models.TextField("Комментарий", null=True, blank=True)
    minutes = models.PositiveSmallIntegerField(
        "Длительность в минутах", null=True, blank=True
    )
    pulse_avg = models.PositiveSmallIntegerField(
        "Пульс в среднем", null=True, blank=True
    )
    pulse_max = models.PositiveSmallIntegerField(
        "Пульс максимальный", null=True, blank=True
    )

    def __str__(self):
        return f"Тренировка клиента {self.client}, {self.date}"

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


class ExerciseReport(models.Model):
    """Запись о проведении упражнения"""

    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    weight = models.DecimalField(
        "Вес в килограммах",
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    approaches_due = models.PositiveSmallIntegerField(
        "Подходы (запланировано)", null=True, blank=True
    )
    approaches_made = models.PositiveSmallIntegerField(
        "Подходы (выполнено)", null=True, blank=True
    )
    repeats_due = models.PositiveSmallIntegerField(
        "Повторы (запланировано)", null=True, blank=True
    )
    repeats_made = models.PositiveSmallIntegerField(
        "Повторы (выполнено)", null=True, blank=True
    )
    load_due = models.PositiveSmallIntegerField(
        "Нагрузка (запланировано)", null=True, blank=True
    )
    load_get = models.PositiveSmallIntegerField(
        "Нагрузка (получено)", null=True, blank=True
    )
    minutes = models.PositiveSmallIntegerField(
        "Длительность в минутах", null=True, blank=True
    )
    pulse_avg = models.PositiveSmallIntegerField(
        "Пульс в среднем", null=True, blank=True
    )
    high_load_time = models.PositiveSmallIntegerField(
        "Время на высокой нагрузке в минутах", null=True, blank=True
    )
    high_load_pulse = models.PositiveSmallIntegerField(
        "Пульс на высокой нагрузке", null=True, blank=True
    )
    low_load_time = models.PositiveSmallIntegerField(
        "Время на низкой нагрузке в минутах", null=True, blank=True
    )
    low_load_pulse = models.PositiveSmallIntegerField(
        "Пульс на низкой нагрузке", null=True, blank=True
    )
    cycles = models.PositiveSmallIntegerField(
        "Повторы цикла", null=True, blank=True
    )
    is_done = models.BooleanField(
        "Упражнение выполнено",
        default=False,
    )

    def __str__(self):
        if self.is_done:
            return f"Выполнено: {self.exercise}, {self.training}"
        else:
            return f"Запланировано: {self.exercise}, {self.training}"

    class Meta:
        verbose_name = "Отчет об упражнении"
        verbose_name_plural = "Отчеты об упражнениях"


# TODO выделить типы в енам
