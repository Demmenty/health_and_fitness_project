# Generated by Django 4.2.5 on 2023-12-06 14:34

from django.db import migrations, models

import metrics.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "metrics",
            "0022_rename_anthropometry_anthropo_rename_dailydata_daily_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="anthropo",
            name="photo_1",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=metrics.models.anthropometry_photo_path,
                verbose_name="Фото спереди",
            ),
        ),
        migrations.AlterField(
            model_name="anthropo",
            name="photo_2",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=metrics.models.anthropometry_photo_path,
                verbose_name="Фото сзади",
            ),
        ),
        migrations.AlterField(
            model_name="anthropo",
            name="photo_3",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=metrics.models.anthropometry_photo_path,
                verbose_name="Фото сбоку",
            ),
        ),
    ]