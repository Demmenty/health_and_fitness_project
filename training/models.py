from django.db import models

from home.utils import resize_uploaded_image
from users.models import User

EXPERT = User.get_expert()

# Map training type to exercise type
EXERCISE_TYPE_MAP = {
    "strength": "strength",
    "endurance": "endurance",
    "round": "strength",
    "interval": "endurance",
}


# CONSTANT (loads from fixtures)
class Area(models.Model):
    """Exercise area"""

    name = models.CharField("Название", max_length=255)
    name_ru = models.CharField("Название (RU)", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_map(cls) -> dict:
        """Get a dictionary mapping area names to their Russian names"""

        return {area.name: area.name_ru for area in cls.objects.all()}

    class Meta:
        verbose_name = "Зона воздействия упражнения"
        verbose_name_plural = "Зоны воздействия упражнений"


class Tool(models.Model):
    """Exercise tool"""

    name = models.CharField("Название", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Инструмент"
        verbose_name_plural = "Инструменты"


class Exercise(models.Model):
    """Physical exercise"""

    class Type(models.TextChoices):
        STRENGTH = "strength", "Сила"
        ENDURANCE = "endurance", "Выносливость"

    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE, default=EXPERT.id
    )
    name = models.CharField("Название", max_length=255, unique=True)
    type = models.CharField(
        "Тип", max_length=9, choices=Type.choices, default=Type.STRENGTH
    )
    tools = models.ManyToManyField("training.Tool", verbose_name="Инструментарий")
    muscles = models.TextField("Целевые мышцы", null=True, blank=True)
    areas = models.ManyToManyField("training.Area", verbose_name="Зоны воздействия")
    description = models.TextField("Техника выполнения")
    mistakes = models.TextField("Частые ошибки", null=True, blank=True)
    icon = models.ImageField(
        "Иконка", upload_to="training/exercise/icons/", null=True, blank=True
    )
    image1 = models.ImageField(
        "Изображение", upload_to="training/exercise/images/", null=True, blank=True
    )
    image2 = models.ImageField(
        "Изображение", upload_to="training/exercise/images/", null=True, blank=True
    )
    video = models.FileField(
        "Видео выполнения", upload_to="training/exercise/videos/", null=True, blank=True
    )
    video_url = models.URLField("Ссылка на видео", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_icon_uploaded = (
            self.icon and self.icon != self.__class__.objects.get(pk=self.pk).icon
        )

        if new_icon_uploaded:
            self.icon = resize_uploaded_image(
                self.icon, self.icon.name, square=True, size=(100, 100)
            )

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class Training(models.Model):
    """Physical training"""

    class Type(models.TextChoices):
        STRENGTH = "strength", "Силовая"
        ENDURANCE = "endurance", "На выносливость"
        ROUND = "round", "Круговая"
        INTERVAL = "interval", "Интервальная"

    exercises = models.ManyToManyField(
        Exercise, through="ExerciseRecord", verbose_name="Упражнения", blank=True
    )

    date = models.DateField("Дата тренировки")
    client = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE)
    type = models.CharField(
        "Тип", max_length=9, choices=Type.choices, default=Type.STRENGTH
    )
    time = models.PositiveSmallIntegerField("Длительность", null=True, blank=True)
    pulse_avg = models.PositiveSmallIntegerField("Средний пульс", null=True, blank=True)
    pulse_max = models.PositiveSmallIntegerField("Макс пульс", null=True, blank=True)
    tiredness = models.PositiveSmallIntegerField("Утомление", null=True, blank=True)
    comment = models.TextField("Комментарий", null=True, blank=True)

    def __str__(self):
        return f"Тренировка клиента {self.client}"

    @classmethod
    def get_schedule(cls, client_id: int, year: int, month: int) -> dict:
        """
        Returns client's training types for a specified month.

        Args:
            client_id (int): The ID of the client.
            year (int): The year of the schedule.
            month (int): The month of the schedule.

        Returns:
            A dictionary representing the schedule:
                keys are the days of the month,
                values are lists of training types.
        """

        trainings = cls.objects.filter(
            client=client_id, date__year=year, date__month=month
        ).values_list("date", "type")

        schedule = {}

        for date, type in trainings:
            schedule.setdefault(date.day, []).append(type)

        return schedule

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


class ExerciseRecord(models.Model):
    """Record about completed physical exercise"""

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    order = models.SmallIntegerField("Порядок", default=1)

    weight = models.DecimalField(
        "Вес", max_digits=4, decimal_places=1, null=True, blank=True
    )
    repetitions = models.PositiveIntegerField("Повторения", null=True, blank=True)
    sets = models.PositiveIntegerField("Подходы", null=True, blank=True)
    load = models.PositiveIntegerField("Нагрузка", null=True, blank=True)
    time = models.PositiveSmallIntegerField("Длительность", null=True, blank=True)
    pulse_avg = models.PositiveSmallIntegerField("Средний пульс", null=True, blank=True)
    high_load_time = models.PositiveSmallIntegerField(
        "Время при высокой нагрузке", null=True, blank=True
    )
    high_load_pulse = models.PositiveSmallIntegerField(
        "Пульс при высокой нагрузке", null=True, blank=True
    )
    low_load_time = models.PositiveSmallIntegerField(
        "Время при низкой нагрузке", null=True, blank=True
    )
    low_load_pulse = models.PositiveSmallIntegerField(
        "Пульс при низкой нагрузке", null=True, blank=True
    )
    cycles = models.PositiveSmallIntegerField("Повторы цикла", null=True, blank=True)
    comment = models.TextField("Комментарий", null=True, blank=True)
    is_done = models.BooleanField("Выполнено", default=False)

    def clear_data(self) -> None:
        """ Clears exercise data in the record (sets, reps, etc) """

        self.weight = None
        self.repetitions = None
        self.sets = None
        self.load = None
        self.time = None
        self.pulse_avg = None
        self.high_load_time = None
        self.high_load_pulse = None
        self.low_load_time = None
        self.low_load_pulse = None
        self.cycles = None
        self.comment = None
        self.is_done = False

    class Meta:
        ordering = ("order", "pk")
        verbose_name = "Запись о выполнении упражнения"
        verbose_name_plural = "Записи о выполнении упражнений"


# TODO
# media preparation

# class AreaTranslation(models.Model):
#     area = models.ForeignKey("training.Area", on_delete=models.CASCADE, related_name="translations")
#     language = models.CharField(max_length=10)
#     name = models.CharField(_("Name"), max_length=255)

#     class Meta:
#         unique_together = [["area", "language"]]

#     def __str__(self):
#         return self.name

# area = Area.objects.get(pk=1)
# english_name = area.name
# russian_name = area.translations.get(language="ru").name
