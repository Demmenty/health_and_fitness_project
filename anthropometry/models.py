from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Anthropometry(models.Model):
    """Модель для данных антропометрических измерений"""

    date = models.DateField("Дата", default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoulder = models.DecimalField(
        "Плечо", max_digits=4, decimal_places=1, null=True, blank=True
    )
    chest = models.DecimalField(
        "Грудь", max_digits=4, decimal_places=1, null=True, blank=True
    )
    waist = models.DecimalField(
        "Талия", max_digits=4, decimal_places=1, null=True, blank=True
    )
    belly = models.DecimalField(
        "Живот", max_digits=4, decimal_places=1, null=True, blank=True
    )
    buttocks = models.DecimalField(
        "Ягодицы", max_digits=4, decimal_places=1, null=True, blank=True
    )
    hip = models.DecimalField(
        "Бедро", max_digits=4, decimal_places=1, null=True, blank=True
    )
    shin = models.DecimalField(
        "Голень", max_digits=4, decimal_places=1, null=True, blank=True
    )
    photo_1 = models.ImageField(
        "Фото №1",
        upload_to="personalpage/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_2 = models.ImageField(
        "Фото №2",
        upload_to="personalpage/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )
    photo_3 = models.ImageField(
        "Фото №3",
        upload_to="personalpage/img/clients/%Y/%d.%m",
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Антропометрия клиента {self.user} за {self.date}"

    class Meta:
        ordering = ["-date"]
        # при запросе должна быть сортировка по убыванию даты
        get_latest_by = "date"


class AnthropometryPhotoAccess(models.Model):
    """Модель для хранения разрешения на просмотр фото к антропометрии эксперту"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_access = models.BooleanField("Доступ эксперта к фото", default=False)

    def __str__(self):
        if self.photo_access:
            return f"Клиент {self.user} разрешил доступ к своим фото"
        else:
            return f"Клиент {self.user} не разрешил доступ к своим фото"
