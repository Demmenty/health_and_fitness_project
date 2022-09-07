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
    date = models.DateField('Дата', default=date.today, help_text='Дата измерения')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Измерение клиента {self.user} за {self.date}"

    class Meta:
        ordering = ['-date']
        #при запросе должна быть сортировка по убыванию даты


class Questionary(models.Model):
    date = models.DateField('Дата заполнения', auto_now_add=True, help_text='Дата заполнения')
    date_update = models.DateField('Дата обновления', auto_now=True, help_text='Дата последнего редактирования')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField('Фамилия Имя Отчество', max_length=200)
    birth_date = models.DateField('Дата рождения')
    parameter12 = models.CharField('Неприятное ощущение сильного или нерегулярного сердцебиения при нагрузке или в покое', max_length=3)
    parameter13 = models.CharField('Одышка при небольшой нагрузке или в покое', max_length=3)
    parameter14 = models.CharField('Потемнения в глазах, головокружения, обмороки, потеря равновесия', max_length=3)
    parameter11 = models.CharField('Дискомфорт или боли в груди при нагрузке или в покое; боль в левой половине нижней челюсти, шеи, левой руке', max_length=3)
    parameter15 = models.CharField('Отечность лодыжек', max_length=3)
    parameter16 = models.CharField('Чувство жжения, боль, судороги в нижних конечностях при ходьбе на малые дистанции', max_length=3)
    parameter17 = models.CharField('Другие известные клиенту причины, по которым ему следует ограничить физическую активность', max_length=3)
    parameter20 = models.CharField('В течение как минимум последних трех месяцев проводятся регулярные тренировки длительностью не менее 30 минут в день, интенсивностью не ниже умеренной, с частотой не менее трех раз в неделю', max_length=3)
    parameter31 = models.CharField('Инфаркт миокарда', max_length=3)
    parameter32 = models.CharField('Катетеризация сердца, коронарная ангиопластика, операции на сердце, трансплантация сердца', max_length=3)
    parameter33 = models.CharField('Нарушения сердечного ритма, кардиостимулятор/имплантируемый сердечный дефибриллятор', max_length=3)
    parameter34 = models.CharField('Врожденные пороки сердца, патологии сердечных клапанов, сердечная недостаточность', max_length=3)
    parameter35 = models.CharField('Сахарный диабет', max_length=3)
    parameter36 = models.CharField('Заболевания почек', max_length=3)
    norm_pressure = models.CharField('Знаете ли Вы свое обычное артериальное давление?', max_length=100)
    parameter42 = models.CharField('Имеются ли у Вас изменения нормального уровня глюкозы в крови?', max_length=100)
    parameter43 = models.CharField('Имеются ли у Вас заболевания мочевыделительной системы?', max_length=255)
    parameter44 = models.CharField('Имеются ли у Вас заболевания дыхательной системы?', max_length=255)
    parameter45 = models.CharField('Имеются ли у Вас заболевания пищеварительной системы?', max_length=255)
    parameter46 = models.CharField('Имеются ли у Вас онкологические заболевания?', max_length=255)
    parameter47 = models.CharField('Имеются ли у Вас заболевания периферических сосудов?', max_length=255)
    parameter48 = models.TextField('Были ли у Вас травмы и хирургические операции?')
    parameter49 = models.CharField('Имеются ли у Вас остеопороз, проблемы со спиной и суставами?', max_length=255)
    parameter410 = models.TextField('Принимаете ли Вы в настоящее время лекарства?')
    parameter411 = models.CharField('Беременны ли Вы?', max_length=100)
    parameter412 = models.CharField('Были ли у Вас роды в последние 6 месяцев?', max_length=255)
    parameter413 = models.TextField('Есть ли у Вас заболевания, не упомянутые в этой анкете?')
    parameter414 = models.TextField('Соблюдаете ли Вы диету?')
    parameter415 = models.TextField('Были ли у Вас в прошлом занятия, связанные с двигательной активностью (спорт, фитнес, танцы, йога и пр.)?')
    parameter416 = models.CharField('Есть ли у Вас в настоящее время занятия, связанные с двигательной активностью (спорт, фитнес, танцы, йога и пр.)?', max_length=6)
    parameter416_exp = models.CharField('Cтаж занятий', max_length=200, default='')
    parameter417 = models.CharField('Имеются ли признаки, которые позволяют заподозрить недовосстановление или перетренированность? (длительная усталость/ощущение утренней разбитости после тренировок, снижение работоспособности, раздражительность или перепады настроения, сильное нежелание тренироваться, нарушения сна)', max_length=255)
    parameter418 = models.CharField('Имеются ли особенности режима работы и отдыха, которые могут повлиять на переносимость нагрузок и восстановление после них? (сменный или ненормированный рабочий день, частые авралы на работе, невозможность полноценного сна, проблемы с регулярным питанием и пр.)', max_length=255)
    parameter419 = models.TextField('Имеются ли не отраженные в анкете моменты, которые могут вызвать трудности при проведении тренировок/тестов на физическую подготовленность?')
    confirm = models.BooleanField('Подверждаю достоверность предоставленных сведений и даю согласие на обработку персональных данных', default=False)

    def __str__(self):
        return f"Анкета клиента {self.user}"


class FatSecretEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_token_secret = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Данные для использования FS клиента {self.user}"


class Anthropometry(models.Model):
    date = models.DateField('Дата', default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoulder = models.DecimalField('Плечо', max_digits=4, decimal_places=1, null=True, blank=True)
    chest = models.DecimalField('Грудь', max_digits=4, decimal_places=1, null=True, blank=True)
    waist = models.DecimalField('Талия', max_digits=4, decimal_places=1, null=True, blank=True)
    belly = models.DecimalField('Живот', max_digits=4, decimal_places=1, null=True, blank=True)
    buttocks = models.DecimalField('Ягодицы', max_digits=4, decimal_places=1, null=True, blank=True)
    hip = models.DecimalField('Бедро', max_digits=4, decimal_places=1, null=True, blank=True)
    shin = models.DecimalField('Голень', max_digits=4, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"Антропометрия клиента {self.user} за {self.date}"

    class Meta:
        ordering = ['-date']
        #при запросе должна быть сортировка по убыванию даты
        get_latest_by = "date"
        