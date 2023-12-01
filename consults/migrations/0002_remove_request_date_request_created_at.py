# Generated by Django 4.2.5 on 2023-12-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("consults", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="request",
            name="date",
        ),
        migrations.AddField(
            model_name="request",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=None, verbose_name="Дата создания"
            ),
            preserve_default=False,
        ),
    ]
