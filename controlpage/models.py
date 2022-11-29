from django.db import models
from datetime import date
from django.contrib.auth.models import User


# модель для комментариев
class Commentary(models.Model):
    date = models.DateField('Дата', default=date.today)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    general = models.TextField('Общее', default='', blank=True)
    general_read = models.BooleanField('Общее - прочитано', default=True)
    measurements = models.TextField('Измерения', default='', blank=True)
    measurements_read = models.BooleanField('Измерения - прочитано', default=True)
    nutrition = models.TextField('Питание', default='', blank=True)
    nutrition_read = models.BooleanField('Питание - прочитано', default=True)
    workout = models.TextField('Тренировки', default='', blank=True)
    workout_read = models.BooleanField('Тренировки - прочитано', default=True)

    def __str__(self):
        return f"Комментарий для клиента {self.client} от {self.date}"

    class Meta:
        ordering = ['-date']
        #при запросе должна быть сортировка по убыванию даты