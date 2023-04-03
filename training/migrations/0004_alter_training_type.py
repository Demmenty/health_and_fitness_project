# Generated by Django 4.1 on 2023-03-26 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0003_powerexercise_weight"),
    ]

    operations = [
        migrations.AlterField(
            model_name="training",
            name="type",
            field=models.CharField(
                choices=[
                    ("P", "Силовая"),
                    ("R", "Круговая"),
                    ("E", "Выносливость"),
                    ("I", "Интервальная"),
                ],
                max_length=2,
                verbose_name="Тип тренировки",
            ),
        ),
    ]