# Generated by Django 4.2.5 on 2023-12-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(blank=True, null=True, verbose_name="Текст"),
        ),
    ]
