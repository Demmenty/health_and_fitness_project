# Generated by Django 4.2.5 on 2023-10-14 09:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("metrics", "0008_alter_dailydata_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ColorSet",
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
                    "parameter",
                    models.CharField(
                        choices=[
                            ("Feel", "Самочувствие"),
                            ("Weight", "Вес"),
                            ("Fat", "Процент жира"),
                            ("Pulse", "Пульс"),
                            ("Pressure_upper", "Давление верхнее"),
                            ("Pressure_lower", "Давление нижнее"),
                            ("Calories", "Калории"),
                            ("Protein", "Белки"),
                            ("Fats", "Жиры"),
                            ("Carbohydrates", "Углеводы"),
                        ],
                        max_length=14,
                        verbose_name="Параметр",
                    ),
                ),
                (
                    "lvl1_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 1: нижняя граница",
                    ),
                ),
                (
                    "lvl1_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 1: верхняя граница",
                    ),
                ),
                (
                    "lvl2_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 2: нижняя граница",
                    ),
                ),
                (
                    "lvl2_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 2: верхняя граница",
                    ),
                ),
                (
                    "lvl3_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 3: нижняя граница",
                    ),
                ),
                (
                    "lvl3_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 3: верхняя граница",
                    ),
                ),
                (
                    "lvl4_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 4: нижняя граница",
                    ),
                ),
                (
                    "lvl4_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 4: верхняя граница",
                    ),
                ),
                (
                    "lvl5_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 5: нижняя граница",
                    ),
                ),
                (
                    "lvl5_max",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Уровень 5: верхняя граница",
                    ),
                ),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Клиент",
                    ),
                ),
            ],
        ),
    ]
