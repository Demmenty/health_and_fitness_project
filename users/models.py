from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models

from home.utils import resize_uploaded_image


def avatars_path(instance, filename):
    """
    Return the path for the user's avatars.
    Example: "users/1/avatar/filename.jpg"
    """

    return f"users/{instance.id}/avatar/{filename}"


class User(AbstractUser):
    """
    Model of a user.
    Could be two main types of users: expert and clients.
    Expert is unique and its existence is mandatory.
    """

    class Sex(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "X", "Другое"

    is_expert = models.BooleanField(verbose_name="Эксперт", default=False)
    email = models.EmailField(
        verbose_name="Почта",
        unique=True,
        error_messages={"unique": "Пользователь с такой почтой уже существует."},
    )
    avatar = models.ImageField("Аватар", upload_to=avatars_path, blank=True, null=True)
    sex = models.CharField("Пол", max_length=1, choices=Sex.choices, null=True)
    birthday = models.DateField("День рождения", null=True)
    height = models.PositiveSmallIntegerField(
        "Рост (см)",
        help_text="Нужен для расчетов, например, индекса массы тела.",
        null=True,
    )

    def __str__(self):
        if self.is_expert:
            return f"Эксперт {self.username.capitalize()}"
        return self.username.capitalize()

    def get_age(self) -> int | None:
        """Return the age of the client or None if no birthday"""

        if not self.birthday:
            return None

        today: date = date.today()
        age: int = today.year - self.birthday.year

        if (today.month < self.birthday.month) or (
            today.month == self.birthday.month and today.day < self.birthday.day
        ):
            age -= 1

        return age

    def save(self, *args, **kwargs):
        new_avatar_uploaded = (
            self.avatar and self.avatar != self.__class__.objects.get(pk=self.pk).avatar
        )

        if new_avatar_uploaded:
            self.avatar = resize_uploaded_image(
                self.avatar, self.avatar.name, square=True, size=(150, 150)
            )

        super().save(*args, **kwargs)

    @classmethod
    def get_expert(cls):
        return User.objects.get(is_expert=True)

    @property
    def is_client(self):
        return not self.is_expert

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
