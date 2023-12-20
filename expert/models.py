from django.db import models

from users.models import User


class ClientMainNote(models.Model):
    """Main expert's note about a client"""

    client = models.OneToOneField(User, verbose_name="Клиент", on_delete=models.CASCADE)
    text = models.TextField("Текст", null=True, blank=True)

    def __str__(self):
        return "Заметка о клиенте"

    class Meta:
        verbose_name = "Заметка о клиенте"
        verbose_name_plural = "Заметки о клиентах"


class ClientMonthlyNote(models.Model):
    """Monthly expert's note about a client by topics"""

    class Month(models.IntegerChoices):
        JANUARY = 1, "Январь"
        FEBRUARY = 2, "Февраль"
        MARCH = 3, "Март"
        APRIL = 4, "Апрель"
        MAY = 5, "Май"
        JUNE = 6, "Июнь"
        JULY = 7, "Июль"
        AUGUST = 8, "Август"
        SEPTEMBER = 9, "Сентябрь"
        OCTOBER = 10, "Октябрь"
        NOVEMBER = 11, "Ноябрь"
        DECEMBER = 12, "Декабрь"

    client = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE)
    month = models.PositiveIntegerField(
        "Месяц", choices=Month.choices, default=Month.JANUARY
    )
    year = models.PositiveSmallIntegerField("Год")
    general = models.TextField("Общее", null=True, blank=True)
    measurements = models.TextField("Измерения", null=True, blank=True)
    nutrition = models.TextField("Питание", null=True, blank=True)
    workout = models.TextField("Тренировки", null=True, blank=True)

    def __str__(self):
        return "Заметка о клиенте"

    class Meta:
        unique_together = ("client", "month", "year")
        verbose_name = "Заметка о клиенте по месяцам"
        verbose_name_plural = "Заметки о клиентах по месяцам"
