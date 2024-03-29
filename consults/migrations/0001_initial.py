# Generated by Django 4.2.5 on 2023-12-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Request",
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
                    "name",
                    models.CharField(
                        help_text="Как к вам обращаться?",
                        max_length=100,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "age",
                    models.CharField(
                        blank=True,
                        help_text="Сколько вам лет?",
                        max_length=100,
                        verbose_name="Возраст",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Расскажите, откуда вы?",
                        max_length=100,
                        verbose_name="Место жительства",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        help_text="Обещаем не использовать адрес в коварных целях!",
                        max_length=100,
                        verbose_name="Почта",
                    ),
                ),
                (
                    "contacts",
                    models.CharField(
                        help_text="Оставьте ссылку на предпочитаемый способ связи",
                        max_length=255,
                        verbose_name="Контакты",
                    ),
                ),
                (
                    "seen",
                    models.BooleanField(default=False, verbose_name="Заявка прочитана"),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, default="", verbose_name="Заметка эксперта"
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
            ],
            options={
                "verbose_name": "Заявка",
                "verbose_name_plural": "Заявки",
            },
        ),
    ]
