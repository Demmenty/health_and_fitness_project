from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(
        verbose_name="Почта",
        unique=True,
        error_messages={
            "unique": "Пользователь с такой почтой уже существует."
        },
    )
    is_expert = models.BooleanField(verbose_name="Эксперт", default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
