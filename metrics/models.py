from datetime import date, datetime
from decimal import Decimal

from django.db import models
from django.forms.models import model_to_dict

from main.utils import resize_uploaded_image
from metrics.managers import DailyMetricsManager
from nutrition.fatsecret import FSManager
from nutrition.models import FatSecretEntry
from users.models import User


class Colors(models.Model):
    """Colors for all metric parameters' indication based on levels."""

    lvl1 = models.CharField(
        "Уровень 1", max_length=7, default="#66e5a2", help_text="идеально"
    )
    lvl2 = models.CharField(
        "Уровень 2",
        max_length=7,
        default="#b2ff99",
        help_text="хорошо",
    )
    lvl3 = models.CharField(
        "Уровень 3",
        max_length=7,
        default="#fffa88",
        help_text="неплохо",
    )
    lvl4 = models.CharField(
        "Уровень 4",
        max_length=7,
        default="#ffd278",
        help_text="плохо",
    )
    lvl5 = models.CharField(
        "Уровень 5",
        max_length=7,
        default="#ff998b",
        help_text="критично",
    )

    def __str__(self):
        return f"Цвета измерений клиентов"

    class Meta:
        verbose_name = "Цвета измерений"
        verbose_name_plural = "Цвета измерений"

    @classmethod
    def get_colors(cls) -> dict:
        """
        Retrieves the colors data as dict.

        Returns:
            dict: The colors data.
        """
        return model_to_dict(cls.objects.get(), exclude=["id"])


class Daily(models.Model):
    """Daily measurements of the client"""

    class Parameters(models.TextChoices):
        FEEL = "feel", "Самочувствие"
        WEIGHT = "weight", "Вес"
        FAT_PERCENTAGE = "fat_percentage", "Процент жира"
        PULSE = "pulse", "Пульс"
        PRESSURE_UPPER = "pressure_upper", "Давление верхнее"
        PRESSURE_LOWER = "pressure_lower", "Давление нижнее"
        CALORIES = "calories", "Калории"
        PROTEIN = "protein", "Белки"
        FAT = "fat", "Жиры"
        CARBS = "carbohydrate", "Углеводы"

    objects = DailyMetricsManager()

    date = models.DateField("Дата измерения", default=date.today)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    feel = models.PositiveSmallIntegerField(
        verbose_name=Parameters.FEEL.label,
        null=True,
        blank=True,
        help_text="Ваше самочувствие в баллах по шкале от 1 до 10",
    )
    weight = models.DecimalField(
        verbose_name=Parameters.WEIGHT.label,
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Ваш вес в килограммах",
    )
    fat_percentage = models.DecimalField(
        verbose_name=Parameters.FAT_PERCENTAGE.label,
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Количество жировой массы в процентах от массы тела",
    )
    pulse = models.PositiveSmallIntegerField(
        verbose_name=Parameters.PULSE.label,
        null=True,
        blank=True,
        help_text="Среднее значение пульса в покое",
    )
    pressure_upper = models.PositiveSmallIntegerField(
        verbose_name=Parameters.PRESSURE_UPPER.label,
        null=True,
        blank=True,
        help_text="Верхнее систолическое давление",
    )
    pressure_lower = models.PositiveSmallIntegerField(
        verbose_name=Parameters.PRESSURE_LOWER.label,
        null=True,
        blank=True,
        help_text="Нижнее диастолическое давление",
    )
    calories = models.PositiveSmallIntegerField(
        verbose_name=Parameters.CALORIES.label,
        null=True,
        blank=True,
        help_text="Количество потребленных за день килокалорий",
    )
    protein = models.DecimalField(
        verbose_name=Parameters.PROTEIN.label,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день белков в граммах",
    )
    fat = models.DecimalField(
        verbose_name=Parameters.FAT.label,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день жиров в граммах",
    )
    carbohydrate = models.DecimalField(
        verbose_name=Parameters.CARBS.label,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Количество потребленных за день углеводов в граммах",
    )
    comment = models.TextField(
        "Комментарий",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Измерениe {self.id}: {self.client}"

    class Meta:
        unique_together = ("client", "date")
        ordering = ("date",)
        get_latest_by = "date"
        verbose_name = "Ежедневные измерения"
        verbose_name_plural = "Ежедневные измерения"

    @classmethod
    def get_avg(
        cls, metrics: tuple["Daily"], count_today_nutrition: bool = True
    ) -> dict:
        """
        Calculate the average value for each field in the given list of metrics.

        Parameters:
            metrics (list["DailyMetrics"]): A list of DailyMetrics objects representing the metrics.
            count_today_nutrition (bool, optional):
                A flag indicating whether to include today's nutrition data in the calculation.
                Defaults to True.
        Returns:
            dict: A dictionary containing the average value for each field in the metrics.
        """
        if not metrics:
            return {}

        metrics_avg = {}
        all_parameters = cls.Parameters.values

        if count_today_nutrition:
            for parameter in all_parameters:
                values = [
                    Decimal(getattr(metric, parameter))
                    for metric in metrics
                    if getattr(metric, parameter) is not None
                ]
                if values:
                    metrics_avg[parameter] = sum(values) / len(values)

        if not count_today_nutrition:
            today = date.today()
            nutrition_parameters = (
                cls.Parameters.CALORIES.value,
                cls.Parameters.PROTEIN.value,
                cls.Parameters.FAT.value,
                cls.Parameters.CARBS.value,
            )
            for parameter in all_parameters:
                values = [
                    Decimal(getattr(metric, parameter))
                    for metric in metrics
                    if metric.date != today or parameter not in nutrition_parameters
                    if getattr(metric, parameter) is not None
                ]
                if values:
                    metrics_avg[parameter] = sum(values) / len(values)

        return metrics_avg

    @classmethod
    def update_nutrition_from_fs(cls, metrics: list["Daily"]) -> list["Daily"]:
        """
        Update the nutrition data of the given list of metrics from the client's FatSecret account.

        Args:
            metrics (list[DailyMetrics]): A list of DailyMetrics objects to be updated.

        Returns:
            list[DailyMetrics]: The updated list of DailyMetrics objects.
        """

        if not metrics:
            return []

        client = metrics[0].client
        client_entry = FatSecretEntry.objects.filter(client=client).first()
        if not client_entry:
            return metrics

        fatsecret = FSManager(client_entry)

        months_in_metrics = {
            datetime(metric.date.year, metric.date.month, 1) for metric in metrics
        }

        for month in months_in_metrics:
            monthly_nutrition = fatsecret.get_monthly_nutrition_dict(month)
            if not monthly_nutrition:
                continue

            for day in metrics:
                day_nutrition = monthly_nutrition.get(day.date)
                if not day_nutrition:
                    continue

                if day.calories != day_nutrition["calories"]:
                    day.calories = day_nutrition["calories"]
                    day.protein = day_nutrition["protein"]
                    day.fat = day_nutrition["fat"]
                    day.carbohydrate = day_nutrition["carbohydrate"]
                    day.save()

        return metrics


class Levels(models.Model):
    """Settings of the parameter's levels for color indication."""

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    parameter = models.CharField(
        "Параметр",
        max_length=14,
        choices=Daily.Parameters.choices,
    )
    lvl1_min = models.PositiveSmallIntegerField(
        "Уровень 1: нижняя граница",
        null=True,
        blank=True,
    )
    lvl1_max = models.PositiveSmallIntegerField(
        "Уровень 1: верхняя граница",
        null=True,
        blank=True,
    )
    lvl2_min = models.PositiveSmallIntegerField(
        "Уровень 2: нижняя граница",
        null=True,
        blank=True,
    )
    lvl2_max = models.PositiveSmallIntegerField(
        "Уровень 2: верхняя граница",
        null=True,
        blank=True,
    )
    lvl3_min = models.PositiveSmallIntegerField(
        "Уровень 3: нижняя граница",
        null=True,
        blank=True,
    )
    lvl3_max = models.PositiveSmallIntegerField(
        "Уровень 3: верхняя граница",
        null=True,
        blank=True,
    )
    lvl4_min = models.PositiveSmallIntegerField(
        "Уровень 4: нижняя граница",
        null=True,
        blank=True,
    )
    lvl4_max = models.PositiveSmallIntegerField(
        "Уровень 4: верхняя граница",
        null=True,
        blank=True,
    )
    lvl5_min = models.PositiveSmallIntegerField(
        "Уровень 5: нижняя граница",
        null=True,
        blank=True,
    )
    lvl5_max = models.PositiveSmallIntegerField(
        "Уровень 5: верхняя граница",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Настройки уровней измерений."

    class Meta:
        unique_together = ("client", "parameter")
        verbose_name = "Настройки уровней измерений"
        verbose_name_plural = "Настройки уровней измерений"

    @classmethod
    def get_levels_as_dict(cls, client: User) -> dict:
        """
        Retrieves the levels associated with a given client as a dictionary.

        Args:
            client (User): The client for which to retrieve the levels.
        Returns:
            dict: A dictionary mapping only levels parameters.
        """
        objects = Levels.objects.filter(client=client)
        if not objects:
            return {}

        excluded_fields = ["id", "client", "parameter"]
        result = {
            obj.parameter: model_to_dict(obj, exclude=excluded_fields) for obj in objects
        }
        return result


def anthropometry_photo_path(instance, filename):
    """
    Return the path for the anthropometry photos of the client.
    Example: "clients/1/anthropometry/2023/filename.jpg"
    """

    return f"clients/{instance.client.id}/anthropometry/{instance.date.year}/{filename}"


class Anthropo(models.Model):
    """Anthropometry measurements of the client"""

    date = models.DateField("Дата", auto_now_add=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
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
        "Фото спереди",
        upload_to=anthropometry_photo_path,
        null=True,
        blank=True,
    )
    photo_2 = models.ImageField(
        "Фото сзади",
        upload_to=anthropometry_photo_path,
        null=True,
        blank=True,
    )
    photo_3 = models.ImageField(
        "Фото сбоку",
        upload_to=anthropometry_photo_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Антропометрия №{self.id}"

    def resize_uploaded_photos(self):
        """Resizes uploaded photos if they are new."""

        old_instance = self.__class__.objects.filter(pk=self.pk).first()
        old_photos = {
            "photo_1": getattr(old_instance, "photo_1", None),
            "photo_2": getattr(old_instance, "photo_2", None),
            "photo_3": getattr(old_instance, "photo_3", None),
        }

        for field_name in ["photo_1", "photo_2", "photo_3"]:
            photo = getattr(self, field_name)
            old_photo = old_photos[field_name]

            is_photo_new = photo and photo != old_photo

            if is_photo_new:
                setattr(
                    self,
                    field_name,
                    resize_uploaded_image(photo, photo.name, max_size=(800, 800)),
                )

    def save(self, *args, **kwargs):
        self.resize_uploaded_photos()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]
        get_latest_by = "date"
        verbose_name = "Антропометрия"
        verbose_name_plural = "Антропометрия"


class PhotoAccess(models.Model):
    """Access to the client's photos for the expert"""

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    is_allowed = models.BooleanField("Доступ эксперта к фото", default=False)

    def __str__(self):
        if self.is_allowed:
            return f"{self.client} разрешил доступ к своим фото"
        else:
            return f"{self.client} не разрешил доступ к своим фото"

    class Meta:
        verbose_name = "Доступ к фото"
        verbose_name_plural = "Доступ к фото"
