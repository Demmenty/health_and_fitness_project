from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models

from main.utils import resize_uploaded_image
from nutrition.cache import FSCacheManager


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
    avatar = models.ImageField(
        "Аватар", upload_to=avatars_path, max_length=200, blank=True, null=True
    )
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

    def resize_uploaded_avatar(self):
        """Resizes uploaded avatar if it is new."""

        avatar = self.avatar
        old_instance = self.__class__.objects.filter(pk=self.pk).first()
        old_avatar = getattr(old_instance, "avatar", None)

        is_avatar_new = avatar and avatar != old_avatar

        if is_avatar_new:
            self.avatar = resize_uploaded_image(
                avatar, avatar.name, max_size=(150, 150), square=True
            )

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.resize_uploaded_avatar()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        FSCacheManager.delete_client_cache(client_id=self.id)

        super().delete(*args, **kwargs)

    @classmethod
    def get_expert(cls):
        return User.objects.get(is_expert=True)

    @property
    def is_client(self):
        return not self.is_expert

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


EXPERT = User.get_expert()
