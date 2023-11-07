# Generated by Django 4.2.5 on 2023-10-14 11:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "metrics",
            "0010_alter_colorset_client_alter_colorset_parameter_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Colors",
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
                    "lvl1",
                    models.CharField(
                        default="#66e5a2",
                        max_length=7,
                        verbose_name="Уровень 1",
                    ),
                ),
                (
                    "lvl2",
                    models.CharField(
                        default="#b2ff99",
                        max_length=7,
                        verbose_name="Уровень 2",
                    ),
                ),
                (
                    "lvl3",
                    models.CharField(
                        default="#fffa88",
                        max_length=7,
                        verbose_name="Уровень 3",
                    ),
                ),
                (
                    "lvl4",
                    models.CharField(
                        default="#ffd278",
                        max_length=7,
                        verbose_name="Уровень 4",
                    ),
                ),
                (
                    "lvl5",
                    models.CharField(
                        default="#ff998b",
                        max_length=7,
                        verbose_name="Уровень 5",
                    ),
                ),
            ],
            options={
                "verbose_name": "Цвета измерений",
                "verbose_name_plural": "Цвета измерений",
            },
        ),
        migrations.RenameModel(
            old_name="ColorSet",
            new_name="Levels",
        ),
    ]
