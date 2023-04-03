# Generated by Django 4.1 on 2023-04-01 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0011_rename_exercise_type_training_training_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExerciseReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        max_digits=4,
                        null=True,
                        verbose_name="Вес в килограммах",
                    ),
                ),
                (
                    "approaches_due",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Подходы (запланировано)",
                    ),
                ),
                (
                    "approaches_made",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Подходы (выполнено)",
                    ),
                ),
                (
                    "repeats_due",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Повторы (запланировано)",
                    ),
                ),
                (
                    "repeats_made",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Повторы (выполнено)",
                    ),
                ),
                (
                    "load_due",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Нагрузка (запланировано)",
                    ),
                ),
                (
                    "load_get",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Нагрузка (получено)",
                    ),
                ),
                (
                    "minutes",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Длительность в минутах",
                    ),
                ),
                (
                    "pulse_avg",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Пульс в среднем"
                    ),
                ),
                (
                    "high_load_time",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Время на высокой нагрузке в минутах",
                    ),
                ),
                (
                    "high_load_pulse",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Пульс на высокой нагрузке",
                    ),
                ),
                (
                    "low_load_time",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Время на низкой нагрузке в минутах",
                    ),
                ),
                (
                    "low_load_pulse",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Пульс на низкой нагрузке",
                    ),
                ),
                (
                    "cycles",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Повторы цикла"
                    ),
                ),
                (
                    "is_done",
                    models.BooleanField(
                        default=False, verbose_name="Упражнение выполнено"
                    ),
                ),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="training.exercise",
                    ),
                ),
                (
                    "training",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="training.training",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="intervalexercisereport",
            name="exercise",
        ),
        migrations.RemoveField(
            model_name="intervalexercisereport",
            name="training",
        ),
        migrations.RemoveField(
            model_name="powerexercisereport",
            name="exercise",
        ),
        migrations.RemoveField(
            model_name="powerexercisereport",
            name="training",
        ),
        migrations.DeleteModel(
            name="EnduranceExerciseReport",
        ),
        migrations.DeleteModel(
            name="IntervalExerciseReport",
        ),
        migrations.DeleteModel(
            name="PowerExerciseReport",
        ),
    ]