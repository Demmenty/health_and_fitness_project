# Generated by Django 4.2.5 on 2023-12-03 05:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metrics", "0016_rename_carbs_dailydata_carbohydrate_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="NutritionRecs",
        ),
    ]
