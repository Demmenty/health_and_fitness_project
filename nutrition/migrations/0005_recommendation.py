# Generated by Django 4.2.5 on 2023-12-03 05:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("nutrition", "0004_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recommendation",
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
                    "calories",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Калории"
                    ),
                ),
                (
                    "protein",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Белки"
                    ),
                ),
                (
                    "fat",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Жиры"
                    ),
                ),
                (
                    "carbohydrate",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Углеводы"
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, default="", verbose_name="Комментарий"),
                ),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Рекомендации КБЖУ",
                "verbose_name_plural": "Рекомендации КБЖУ",
            },
        ),
    ]