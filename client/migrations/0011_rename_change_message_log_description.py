# Generated by Django 4.2.5 on 2023-11-29 07:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0010_health_is_filled"),
    ]

    operations = [
        migrations.RenameField(
            model_name="log",
            old_name="change_message",
            new_name="description",
        ),
    ]
