# Generated by Django 4.1 on 2023-03-31 17:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0008_alter_training_comment"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="EnduranceExercise",
            new_name="EnduranceExerciseReport",
        ),
        migrations.RenameModel(
            old_name="intervalExercise",
            new_name="IntervalExerciseReport",
        ),
        migrations.RenameModel(
            old_name="PowerExercise",
            new_name="PowerExerciseReport",
        ),
    ]
