# Generated by Django 4.2.5 on 2023-10-13 05:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metrics", "0007_alter_dailydata_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dailydata",
            options={
                "get_latest_by": "date",
                "ordering": ("date",),
                "verbose_name": "Ежедневные измерения",
                "verbose_name_plural": "Ежедневные измерения",
            },
        ),
        migrations.AlterField(
            model_name="dailydata",
            name="carbohydrates",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Количество потребленных за день углеводов в граммах",
                max_digits=6,
                null=True,
                verbose_name="Углеводы",
            ),
        ),
        migrations.AlterField(
            model_name="dailydata",
            name="fats",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Количество потребленных за день жиров в граммах",
                max_digits=6,
                null=True,
                verbose_name="Жиры",
            ),
        ),
        migrations.AlterField(
            model_name="dailydata",
            name="protein",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Количество потребленных за день белков в граммах",
                max_digits=6,
                null=True,
                verbose_name="Белки",
            ),
        ),
    ]
