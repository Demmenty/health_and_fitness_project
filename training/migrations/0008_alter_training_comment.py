# Generated by Django 4.1 on 2023-03-31 11:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "training",
            "0007_exercise_mistakes_exercise_photo_init_pose_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="training",
            name="comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="Комментарий"
            ),
        ),
    ]
