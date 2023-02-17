from django.db import models
from django.contrib.auth.models import User


class ClientContact(models.Model):
    """модель для хранения контактов клиента"""

    CONTACT_CHOICES = [
        ('TG', 'Telegram'),
        ('WA', 'Whatsapp'),
        ('DC', 'Discord'),
        ('SK', 'Skype'),
        ('VK', 'Vkontakte'),
        ('FB', 'Facebook'),
        ('No', 'не выбрано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram = models.URLField('Telegram', max_length=250, null=True, blank=True)
    whatsapp = models.URLField('Whatsapp', max_length=250, null=True, blank=True)
    discord = models.CharField('Discord', max_length=250, null=True, blank=True)
    skype = models.URLField('Skype', max_length=250, null=True, blank=True)
    vkontakte = models.URLField('Vkontakte', max_length=250, null=True, blank=True)
    facebook = models.URLField('Facebook', max_length=250, null=True, blank=True)
    preferred_contact = models.CharField('Предпочтительный способ связи', choices=CONTACT_CHOICES, default='No', max_length=2)

    def __str__(self):
        return f"Контакты клиента {self.user}"


class HealthQuestionary(models.Model):
    """модель для хранения данных анкеты здоровья клиента"""
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
    parameter416_exp = models.CharField('Cтаж занятий', max_length=200, default="", blank=True)
    parameter417 = models.CharField('Имеются ли признаки, которые позволяют заподозрить недовосстановление или перетренированность? (длительная усталость/ощущение утренней разбитости после тренировок, снижение работоспособности, раздражительность или перепады настроения, сильное нежелание тренироваться, нарушения сна)', max_length=255)
    parameter418 = models.CharField('Имеются ли особенности режима работы и отдыха, которые могут повлиять на переносимость нагрузок и восстановление после них? (сменный или ненормированный рабочий день, частые авралы на работе, невозможность полноценного сна, проблемы с регулярным питанием и пр.)', max_length=255)
    parameter419 = models.TextField('Имеются ли не отраженные в анкете моменты, которые могут вызвать трудности при проведении тренировок/тестов на физическую подготовленность?')
    confirm = models.BooleanField('Подверждаю достоверность предоставленных сведений и даю согласие на обработку персональных данных', default=False)

    def __str__(self):
        return f"Анкета здоровья клиента {self.user}"
