from django.db import models
from django.utils import timezone

from users.models import User


class Plan(models.Model):
    """Model of a subscription plan for access to app"""

    class Access(models.TextChoices):
        NUTRITION = "NUTRITION", "Питание"
        TRAININGS = "TRAINING", "Тренировки"
        FULL = "FULL", "Полный"

    class Coaching(models.TextChoices):
        NONE = "NONE", "Нет"
        NUTRITION = "NUTRITION", "Питание"
        TRAININGS = "TRAINING", "Тренировки"
        FULL = "FULL", "Полное"

    name = models.CharField("Название", max_length=255)
    access = models.CharField(
        "Доступ",
        max_length=9,
        choices=Access.choices,
        default=Access.FULL,
        help_text="Доступные клиенту модули приложения.",
    )
    coaching = models.CharField(
        "Сопровождение",
        max_length=9,
        choices=Coaching.choices,
        default=Coaching.NONE,
        help_text="Осуществляемое экспертом сопровождение.",
    )
    default_price = models.PositiveSmallIntegerField(
        "Цена", default=0, help_text="Стандартная цена подписки за месяц."
    )
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return f"Тарифный план '{self.name}'"

    class Meta:
        verbose_name = "Тарифный план"
        verbose_name_plural = "Тарифные планы"


class Subscription(models.Model):
    """Model of a subscription details for specific client"""

    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="subscription",
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, verbose_name="План", null=True, blank=True
    )
    price = models.PositiveSmallIntegerField(
        "Цена",
        null=True,
        blank=True,
        help_text="Индивидуальная цена подписки за месяц. По умолчанию - стандартная цена тарифного плана.",
    )
    start_date = models.DateTimeField(
        "Дата начала",
        default=timezone.now,
        help_text="Дата начала подписки. По умолчанию - текущая дата.",
    )
    end_date = models.DateTimeField(
        "Дата окончания",
        null=True,
        blank=True,
        help_text="Дата окончания подписки. По умолчанию - бессрочно.",
    )
    comment = models.TextField(
        "Комментарий",
        null=True,
        blank=True,
        help_text="Комментарий тоже будет виден клиенту.",
    )

    def __str__(self):
        return f"Подписка №{self.id}"

    def save(self, *args, **kwargs):
        if self.plan and not self.price:
            self.price = self.plan.default_price

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Подписка клиента"
        verbose_name_plural = "Подписки клиентов"
