from tkinter import CASCADE
from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Measurement(models.Model):
    weight = models.DecimalField('Вес', max_digits=4, decimal_places=1, null=True, blank=True, help_text='Ваш вес в килограммах')
    fat = models.DecimalField('Жир', max_digits=3, decimal_places=1, null=True, blank=True, help_text='Количество жировой массы в процентах от массы тела')
    feel = models.PositiveSmallIntegerField('Самочувствие', null=True, blank=True, help_text='Ваше самочувствие в баллах по шкале от 1 до 10')
    pulse = models.PositiveSmallIntegerField('Пульс', null=True, blank=True, help_text='Среднее значение пульса в покое')
    pressure_upper = models.PositiveSmallIntegerField('Давление верхнее', null=True, blank=True, help_text='Верхнее систолическое давление')
    pressure_lower = models.PositiveSmallIntegerField('Давление нижнее', null=True, blank=True, help_text='Нижнее диастолическое давление')
    calories = models.PositiveSmallIntegerField('Калории', null=True, blank=True, help_text='Количество потребленных за день килокалорий')
    protein = models.DecimalField('Белки', max_digits=5, decimal_places=2, null=True, blank=True, help_text='Количество потребленных за день белков в граммах')
    fats = models.DecimalField('Жиры', max_digits=5, decimal_places=2, null=True, blank=True, help_text='Количество потребленных за день жиров в граммах')
    carbohydrates = models.DecimalField('Углеводы', max_digits=5, decimal_places=2, null=True, blank=True, help_text='Количество потребленных за день углеводов в граммах')
    comment = models.TextField('Комментарий', default='', blank=True, help_text='Комментарий (при необходимости)')
    date = models.DateField('Дата', default=date.today, help_text='Дата, по умолчанию будет указана сегодняшняя')
    weekday = models.CharField('День недели', max_length=15, default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Измерение клиента {self.user} за {self.date}"

    class Meta:
        ordering = ['-date']
        #при запросе должна быть сортировка по убыванию даты


