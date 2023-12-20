# Generated by Django 4.2.5 on 2023-12-19 14:58

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
            name="ClientNote",
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
                ("text", models.TextField(blank=True, null=True, verbose_name="Текст")),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заметка о клиенте",
                "verbose_name_plural": "Заметки о клиентах",
            },
        ),
        migrations.CreateModel(
            name="ClientMonthlyNote",
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
                    "month",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "Январь"),
                            (2, "Февраль"),
                            (3, "Март"),
                            (4, "Апрель"),
                            (5, "Май"),
                            (6, "Июнь"),
                            (7, "Июль"),
                            (8, "Август"),
                            (9, "Сентябрь"),
                            (10, "Октябрь"),
                            (11, "Ноябрь"),
                            (12, "Декабрь"),
                        ],
                        verbose_name="Месяц",
                    ),
                ),
                ("year", models.PositiveSmallIntegerField(verbose_name="Год")),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("general", "Общее"),
                            ("measurements", "Измерения"),
                            ("nutrition", "Питание"),
                            ("workout", "Тренировки"),
                        ],
                        default="general",
                        max_length=12,
                        verbose_name="Тема",
                    ),
                ),
                ("text", models.TextField(blank=True, null=True, verbose_name="Текст")),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заметка о клиенте за месяц",
                "verbose_name_plural": "Заметки о клиентах за месяцы",
                "unique_together": {("client", "month", "topic")},
            },
        ),
    ]
