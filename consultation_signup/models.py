from django.db import models


# модель для записей на консультацию
class ConsultationSignup(models.Model):
    date = models.DateField('Дата заполнения заявки', auto_now_add=True)
    name = models.CharField('Имя', max_length=100, help_text='Как к вам обращаться?')
    age = models.CharField('Возраст', max_length=100, blank=True, help_text='Сколько вам лет?')
    location = models.CharField('Место жительства', max_length=100, blank=True, help_text='Расскажите, откуда вы?')
    email = models.EmailField('Почта', max_length=100, blank=True, help_text='Обещаем не использовать адрес в коварных целях!')
    contacts = models.CharField('Контакты', max_length=255, help_text='Оставьте ссылку на предпочитаемый способ связи')
    is_read = models.BooleanField('Заявка прочитана', default=False)
    expert_note = models.TextField('Заметка', default='', blank=True)

    def __str__(self):
        return f"Заявка № {self.id} от {self.date}, {self.name}"
        