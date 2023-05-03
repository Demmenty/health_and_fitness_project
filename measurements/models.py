from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Measurement(models.Model):
    """Модель для ежедневных измерений физических показателей"""

    weight = models.DecimalField(
        "Вес",
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Ваш вес в килограммах",
    )
    fat = models.DecimalField(
        "Жир",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Количество жировой массы в процентах от массы тела",
    )
    feel = models.PositiveSmallIntegerField(
        "Самочувствие",
        null=True,
        blank=True,
        help_text="Ваше самочувствие в баллах по шкале от 1 до 10",
    )
    pulse = models.PositiveSmallIntegerField(
        "Пульс",
        null=True,
        blank=True,
        help_text="Среднее значение пульса в покое",
    )
    pressure_upper = models.PositiveSmallIntegerField(
        "Давление верхнее",
        null=True,
        blank=True,
        help_text="Верхнее систолическое давление",
    )
    pressure_lower = models.PositiveSmallIntegerField(
        "Давление нижнее",
        null=True,
        blank=True,
        help_text="Нижнее диастолическое давление",
    )
    calories = models.PositiveSmallIntegerField(
        "Калории",
        null=True,
        blank=True,
        help_text="Количество потребленных за день килокалорий",
    )
    protein = models.DecimalField(
        "Белки",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день белков в граммах",
    )
    fats = models.DecimalField(
        "Жиры",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день жиров в граммах",
    )
    carbohydrates = models.DecimalField(
        "Углеводы",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день углеводов в граммах",
    )
    comment = models.TextField(
        "Комментарий",
        default="",
        blank=True,
        help_text="Комментарий (при необходимости)",
    )
    date = models.DateField(
        "Дата", default=date.today, help_text="Дата измерения"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Измерение клиента {self.user} за {self.date}"

    class Meta:
        ordering = ["-date"]
        verbose_name = "Дневное измерение физических показателей"
        verbose_name_plural = "Дневные измерения физических показателей"


class MeasureColor(models.Model):
    """Модель для хранения вариантов окрашивания показателей"""

    color = models.CharField("Цвет фона", max_length=20, default="#ffffff00")
    meaning = models.CharField("Значение фона", max_length=100)

    def __str__(self):
        return f"{self.meaning}"

    class Meta:
        verbose_name = "Окрашивание дневных измерений"
        verbose_name_plural = "Окрашивания дневных измерений"


class MeasureIndex(models.Model):
    """Модель для вариантов показателей измерений для окрашивания"""

    index_name = models.CharField("Показатель", max_length=50)

    def __str__(self):
        return f"{self.index_name}"

    class Meta:
        verbose_name = "Показатель измерений"
        verbose_name_plural = "Показатели измерений"


class MeasureColorField(models.Model):
    """Модель для хранения соответствий цвета, показателей и клиента"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.ForeignKey(MeasureIndex, on_delete=models.CASCADE)
    color = models.ForeignKey(
        MeasureColor, on_delete=models.CASCADE, default="1"
    )
    low_limit = models.DecimalField(
        "Нижняя граница включительно",
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        default=None,
    )
    upper_limit = models.DecimalField(
        "Верхняя граница включительно",
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f"Настройки цвета для клиента {self.user}: {self.color}, {self.index}"

    class Meta:
        verbose_name = "Границы цветов измерений для клиента"
        verbose_name_plural = "Границы цветов измерений для клиентов"


class Anthropometry(models.Model):
    """Модель для данных антропометрических измерений"""

    date = models.DateField("Дата", default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoulder = models.DecimalField(
        "Плечо", max_digits=4, decimal_places=1, null=True, blank=True
    )
    chest = models.DecimalField(
        "Грудь", max_digits=4, decimal_places=1, null=True, blank=True
    )
    waist = models.DecimalField(
        "Талия", max_digits=4, decimal_places=1, null=True, blank=True
    )
    belly = models.DecimalField(
        "Живот", max_digits=4, decimal_places=1, null=True, blank=True
    )
    buttocks = models.DecimalField(
        "Ягодицы", max_digits=4, decimal_places=1, null=True, blank=True
    )
    hip = models.DecimalField(
        "Бедро", max_digits=4, decimal_places=1, null=True, blank=True
    )
    shin = models.DecimalField(
        "Голень", max_digits=4, decimal_places=1, null=True, blank=True
    )
    photo_1 = models.ImageField(
        "Фото №1",
        upload_to="anthropometry/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_2 = models.ImageField(
        "Фото №2",
        upload_to="anthropometry/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_3 = models.ImageField(
        "Фото №3",
        upload_to="anthropometry/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Антропометрия клиента {self.user} за {self.date}"

    class Meta:
        ordering = ["-date"]
        # при запросе должна быть сортировка по убыванию даты
        get_latest_by = "date"
        verbose_name = "Антропометрия"
        verbose_name_plural = "Антропометрии"


class AnthropometryPhotoAccess(models.Model):
    """Модель для хранения разрешения на просмотр фото к антропометрии эксперту"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_access = models.BooleanField("Доступ эксперта к фото", default=False)

    def __str__(self):
        if self.photo_access:
            return f"Клиент {self.user} разрешил доступ к своим фото"
        else:
            return f"Клиент {self.user} не разрешил доступ к своим фото"

    class Meta:
        verbose_name = "Доступ к фото"
        verbose_name_plural = "Доступы к фото"
