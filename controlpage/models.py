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


# модель для записей на консультацию
class Consultationsignup(models.Model):
    date = models.DateField('Дата заполнения заявки', auto_now_add=True)
    name = models.CharField('Имя', max_length=100, help_text='Как к вам обращаться?')
    age = models.CharField('Возраст', max_length=100, blank=True, help_text='Сколько вам лет?')
    location = models.CharField('Место жительства', max_length=100, blank=True, help_text='Расскажите, откуда вы?')
    email = models.EmailField('Почта', max_length=100, blank=True, help_text='Обещаем не использовать в коварных целях!')
    contacts = models.CharField('Контакты', max_length=255, help_text='Оставьте ссылку на предпочитаемый способ связи')
    is_read = models.BooleanField('Заявка прочитана', default=False)
    expert_comment = models.TextField('Комментарий', null=True, blank=True)

    def __str__(self):
        return f"Заявка № {self.id}, дата: {self.date}, имя: {self.name}"

