# Generated by Django 4.2.5 on 2023-12-26 12:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0006_goal"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="food",
            options={
                "verbose_name": "Данные о питании",
                "verbose_name_plural": "Питание",
            },
        ),
        migrations.AlterModelOptions(
            name="goal",
            options={"verbose_name": "Данные о целях", "verbose_name_plural": "Цели"},
        ),
        migrations.AlterModelOptions(
            name="health",
            options={
                "verbose_name": "Данные о здоровье",
                "verbose_name_plural": "Здоровье",
            },
        ),
        migrations.AlterModelOptions(
            name="note",
            options={"verbose_name": "Заметка", "verbose_name_plural": "Личные заметки"},
        ),
        migrations.AlterModelOptions(
            name="sleep",
            options={"verbose_name": "Данные о сне", "verbose_name_plural": "Сон"},
        ),
        migrations.AlterModelOptions(
            name="weight",
            options={"verbose_name": "Данные о весе", "verbose_name_plural": "Вес"},
        ),
    ]
