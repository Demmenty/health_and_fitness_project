# Generated by Django 4.1 on 2023-04-01 15:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0010_rename_type_exercise_exercise_type_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="training",
            old_name="exercise_type",
            new_name="training_type",
        ),
    ]
