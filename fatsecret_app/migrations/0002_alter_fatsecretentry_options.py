# Generated by Django 4.1 on 2023-04-27 06:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fatsecret_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fatsecretentry",
            options={
                "verbose_name": "Данные для входа в Fatsecret",
                "verbose_name_plural": "Данные для входа в Fatsecret",
            },
        ),
    ]