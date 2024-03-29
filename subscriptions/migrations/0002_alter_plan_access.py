# Generated by Django 4.2.5 on 2024-02-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="access",
            field=models.CharField(
                choices=[
                    ("NUTRITION", "Питание"),
                    ("TRAINING", "Тренировки"),
                    ("FULL", "Полный"),
                ],
                default="FULL",
                help_text="Доступные клиенту модули приложения.",
                max_length=9,
                verbose_name="Доступ",
            ),
        ),
    ]
