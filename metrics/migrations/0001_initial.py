# Generated by Django 4.2.5 on 2023-10-08 17:32

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        help_text="Ваш вес в килограммах",
                        max_digits=4,
                        null=True,
                        verbose_name="Вес",
                    ),
                ),
                (
                    "fat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        help_text="Количество жировой массы в процентах от массы тела",
                        max_digits=3,
                        null=True,
                        verbose_name="Жир",
                    ),
                ),
                (
                    "feel",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="Ваше самочувствие в баллах по шкале от 1 до 10",
                        null=True,
                        verbose_name="Самочувствие",
                    ),
                ),
                (
                    "pulse",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="Среднее значение пульса в покое",
                        null=True,
                        verbose_name="Пульс",
                    ),
                ),
                (
                    "pressure_upper",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="Верхнее систолическое давление",
                        null=True,
                        verbose_name="Давление верхнее",
                    ),
                ),
                (
                    "pressure_lower",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="Нижнее диастолическое давление",
                        null=True,
                        verbose_name="Давление нижнее",
                    ),
                ),
                (
                    "calories",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="Количество потребленных за день килокалорий",
                        null=True,
                        verbose_name="Калории",
                    ),
                ),
                (
                    "protein",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Количество потребленных за день белков в граммах",
                        max_digits=5,
                        null=True,
                        verbose_name="Белки",
                    ),
                ),
                (
                    "fats",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Количество потребленных за день жиров в граммах",
                        max_digits=5,
                        null=True,
                        verbose_name="Жиры",
                    ),
                ),
                (
                    "carbohydrates",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Количество потребленных за день углеводов в граммах",
                        max_digits=5,
                        null=True,
                        verbose_name="Углеводы",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, null=True, verbose_name="Комментарий"
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=datetime.date.today,
                        verbose_name="Дата измерения",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Ежедневные измерения",
                "verbose_name_plural": "Ежедневные измерения",
                "ordering": ["-date"],
            },
        ),
    ]
