# Generated by Django 4.2.5 on 2023-12-11 15:42

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
            name="Area",
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
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "name_ru",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Название (RU)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Зона воздействия упражнения",
                "verbose_name_plural": "Зоны воздействия упражнений",
            },
        ),
        migrations.CreateModel(
            name="Exercise",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("strength", "Сила"), ("endurance", "Выносливость")],
                        default="strength",
                        max_length=9,
                        verbose_name="Тип",
                    ),
                ),
                (
                    "muscles",
                    models.TextField(
                        blank=True, null=True, verbose_name="Целевые мышцы"
                    ),
                ),
                ("description", models.TextField(verbose_name="Техника выполнения")),
                (
                    "mistakes",
                    models.TextField(
                        blank=True, null=True, verbose_name="Частые ошибки"
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="training/exercise/icons/",
                        verbose_name="Иконка",
                    ),
                ),
                (
                    "image1",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="training/exercise/images/",
                        verbose_name="Фото/гифка",
                    ),
                ),
                (
                    "image2",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="training/exercise/images/",
                        verbose_name="Фото/гифка",
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="training/exercise/videos/",
                        verbose_name="Видео выполнения",
                    ),
                ),
                (
                    "video_url",
                    models.URLField(
                        blank=True, null=True, verbose_name="Ссылка на видео"
                    ),
                ),
                (
                    "areas",
                    models.ManyToManyField(
                        to="training.area", verbose_name="Зоны воздействия"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение",
                "verbose_name_plural": "Упражнения",
            },
        ),
        migrations.CreateModel(
            name="ExerciseRecord",
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
                        max_digits=4,
                        null=True,
                        verbose_name="Вес",
                    ),
                ),
                (
                    "repetitions",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Повторения"
                    ),
                ),
                (
                    "sets",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Подходы"
                    ),
                ),
                (
                    "load",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Нагрузка"
                    ),
                ),
                (
                    "time",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Длительность (мин)"
                    ),
                ),
                (
                    "pulse_avg",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс (средний)"
                    ),
                ),
                (
                    "high_load_time",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Время при высокой нагрузке (мин)",
                    ),
                ),
                (
                    "high_load_pulse",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс при высокой нагрузке"
                    ),
                ),
                (
                    "low_load_time",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Время при низкой нагрузке (мин)",
                    ),
                ),
                (
                    "low_load_pulse",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс при низкой нагрузке"
                    ),
                ),
                (
                    "cycles",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Повторы цикла"
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
                (
                    "is_done",
                    models.BooleanField(
                        default=False, verbose_name="Упражнение выполнено"
                    ),
                ),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="training.exercise",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запись о выполнении упражнения",
                "verbose_name_plural": "Записи о выполнении упражнений",
            },
        ),
        migrations.CreateModel(
            name="Tool",
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
                ("name", models.CharField(max_length=255, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Инструмент",
                "verbose_name_plural": "Инструменты",
            },
        ),
        migrations.CreateModel(
            name="Training",
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
                ("date", models.DateField(verbose_name="Дата тренировки")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("strength", "Силовая"),
                            ("endurance", "На выносливость"),
                            ("round", "Круговая"),
                            ("interval", "Интервальная"),
                        ],
                        default="strength",
                        max_length=9,
                        verbose_name="Тип",
                    ),
                ),
                (
                    "time",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Длительность (мин)"
                    ),
                ),
                (
                    "pulse_avg",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс (средний)"
                    ),
                ),
                (
                    "pulse_max",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс (макс)"
                    ),
                ),
                (
                    "tiredness",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Утомление"
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Клиент",
                    ),
                ),
                (
                    "exercises",
                    models.ManyToManyField(
                        blank=True,
                        through="training.ExerciseRecord",
                        to="training.exercise",
                        verbose_name="Упражнения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тренировка",
                "verbose_name_plural": "Тренировки",
            },
        ),
        migrations.AddField(
            model_name="exerciserecord",
            name="training",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="training.training"
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="tools",
            field=models.ManyToManyField(
                to="training.tool", verbose_name="Инструментарий"
            ),
        ),
    ]
