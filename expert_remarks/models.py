from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Commentary(models.Model):
    """Модель для комментариев от эксперта клиенту"""

    date = models.DateField("Дата", default=date.today)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    general = models.TextField("Общее", default="", blank=True)
    general_read = models.BooleanField("Общее - прочитано", default=True)
    measurements = models.TextField("Измерения", default="", blank=True)
    measurements_read = models.BooleanField(
        "Измерения - прочитано", default=True
    )
    nutrition = models.TextField("Питание", default="", blank=True)
    nutrition_read = models.BooleanField("Питание - прочитано", default=True)
    workout = models.TextField("Тренировки", default="", blank=True)
    workout_read = models.BooleanField("Тренировки - прочитано", default=True)

    def __str__(self):
        return f"Комментарий для клиента {self.client} от {self.date}"

    class Meta:
        ordering = ["-date"]


class Clientnote(models.Model):
    """Модель для заметок эксперта о клиенте по месяцам"""

    # даты - по месяцам, добавляя первое число к каждому
    date = models.DateField("Дата")
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    general = models.TextField("Общее", default="", blank=True)
    measurements = models.TextField("Измерения", default="", blank=True)
    nutrition = models.TextField("Питание", default="", blank=True)
    workout = models.TextField("Тренировки", default="", blank=True)

    def __str__(self):
        return (
            f"Заметка о клиенте {self.client} за {self.date.strftime('%B %Y')}"
        )

    class Meta:
        ordering = ["-date"]


class FullClientnote(models.Model):
    """Модель для заметок эксперта о клиенте совокупная"""

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField("Заметка", default="", blank=True)

    def __str__(self):
        return f"Заметка о клиенте {self.client}"
