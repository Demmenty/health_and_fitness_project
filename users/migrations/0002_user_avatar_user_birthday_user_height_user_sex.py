# Generated by Django 4.2.5 on 2023-11-30 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="users/avatars", verbose_name="Аватар"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(null=True, verbose_name="День рождения"),
        ),
        migrations.AddField(
            model_name="user",
            name="height",
            field=models.PositiveSmallIntegerField(
                help_text="Нужен для расчетов, например, индекса массы тела.",
                null=True,
                verbose_name="Рост (см)",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="sex",
            field=models.CharField(
                choices=[("M", "Мужской"), ("F", "Женский"), ("X", "Другое")],
                max_length=1,
                null=True,
                verbose_name="Пол",
            ),
        ),
    ]
