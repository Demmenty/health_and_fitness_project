from django.contrib.auth.models import AbstractUser
from django.db import models


# TODO add avatar with default values
class User(AbstractUser):
    """
    Model of a user.
    Could be two main types of users: expert and clients.
    Expert is unique and its existence is mandatory.
    """

    email = models.EmailField(
        verbose_name="Почта",
        unique=True,
        error_messages={"unique": "Пользователь с такой почтой уже существует."},
    )
    is_expert = models.BooleanField(verbose_name="Эксперт", default=False)

    def __str__(self):
        if self.is_expert:
            return f"Эксперт {self.username}"
        return f"Клиент {self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @classmethod
    def get_expert(cls):
        return User.objects.get(is_expert=True)
