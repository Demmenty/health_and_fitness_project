from django.db import models
from django.utils.timezone import now

from users.models import User


class Note(models.Model):
    """Client's personal note"""

    client = models.OneToOneField(User, verbose_name="Клиент", on_delete=models.CASCADE)
    general = models.TextField("Общее", null=True, blank=True)
    measurements = models.TextField("Измерения", null=True, blank=True)
    nutrition = models.TextField("Питание", null=True, blank=True)
    workout = models.TextField("Тренировки", null=True, blank=True)

    def __str__(self):
        return "Заметка"

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"


class Health(models.Model):
    """Health information about the client and readiness to workout"""

    class CurrentPhysicalActivity(models.TextChoices):
        HIGH = (
            "H",
            "3 занятия в неделю или больше, занятия регулярные, нагрузки от значительных до предельных",
        )
        MEDIUM = (
            "M",
            "2–3 занятия в неделю, занятия достаточно регулярные, нагрузки от умеренных до значительных",
        )
        LOW = (
            "L",
            "меньше 2 занятий в неделю, занятия нерегулярные, нагрузки от незначительных до умеренных",
        )
        NONE = "N", "нет занятий"

    class WorkoutReadiness(models.TextChoices):
        HIGH = "H", "Высокий уровень"
        MEDIUM = "M", "Средний уровень"
        LOW = "L", "Низкий уровень"

    # 0. Start of the health questionnaire
    client = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, verbose_name="Клиент"
    )
    confirmation = models.BooleanField(
        "Подверждаю достоверность предоставляемых сведений и даю согласие на обработку персональных данных.",
        default=False,
    )

    # 1. The presence of potentially dangerous subjective feelings.
    palpitation = models.BooleanField(
        "Неприятное ощущение сильного или нерегулярного сердцебиения при нагрузке или в покое.",
        default=False,
    )
    dyspnea = models.BooleanField(
        "Одышка при небольшой нагрузке или в покое.", default=False
    )
    fainting = models.BooleanField(
        "Потемнения в глазах, головокружения, обмороки, потеря равновесия.",
        default=False,
    )
    chest_pain = models.BooleanField(
        "Дискомфорт или боли в груди при нагрузке или в покое; боль в левой половине нижней челюсти, шеи, левой руке.",
        default=False,
    )
    ankles_swelling = models.BooleanField("Отечность лодыжек.", default=False)
    leg_cramps = models.BooleanField(
        "Чувство жжения, боль, судороги в нижних конечностях при ходьбе на малые дистанции.",
        default=False,
    )
    restriction_reasons = models.BooleanField(
        "Другие известные причины, по которым следует ограничить физическую активность.",
        default=False,
    )

    # 2. The presence of diagnosed health conditions.
    heart_attack = models.BooleanField("Инфаркт миокарда.", default=False)
    cardiac_surgery = models.BooleanField(
        "Катетеризация сердца, коронарная ангиопластика, операции на сердце, трансплантация сердца.",
        default=False,
    )
    pacemaker = models.BooleanField(
        "Кардиостимулятор/имплантируемый сердечный дефибриллятор.",
        default=False,
    )
    arrhythmia = models.BooleanField("Нарушения сердечного ритма.", default=False)
    heart_defect = models.BooleanField(
        "Врожденные пороки сердца, патологии сердечных клапанов, сердечная недостаточность.",
        default=False,
    )
    diabetes = models.BooleanField("Сахарный диабет.", default=False)
    kidney_disease = models.BooleanField("Заболевания почек.", default=False)

    # 3 Additional health information.
    known_blood_pressure = models.BooleanField(
        "Знаете ли Вы свое обычное артериальное давление?", default=False
    )
    blood_pressure = models.CharField(
        "Ваше обычное артериальное давление",
        max_length=100,
        blank=True,
        null=True,
    )
    has_glucose_changes = models.BooleanField(
        "Имеются ли у Вас изменения нормального уровня глюкозы в крови?",
        default=False,
    )
    glucose_level = models.CharField(
        "Укажите свой уровень сахара в крови",
        max_length=100,
        blank=True,
        null=True,
    )
    has_urinary_diseases = models.BooleanField(
        "Имеются ли у Вас заболевания мочевыделительной системы?",
        default=False,
    )
    urinary_diseases = models.CharField(
        "Перечислите имеющиеся заболевания мочевыделительной системы",
        max_length=255,
        blank=True,
        null=True,
    )
    has_respiratory_diseases = models.BooleanField(
        "Имеются ли у Вас заболевания дыхательной системы?", default=False
    )
    respiratory_diseases = models.CharField(
        "Перечислите имеющиеся заболевания дыхательной системы",
        max_length=255,
        blank=True,
        null=True,
    )
    has_digestive_diseases = models.BooleanField(
        "Имеются ли у Вас заболевания пищеварительной системы?", default=False
    )
    digestive_diseases = models.CharField(
        "Перечислите имеющиеся заболевания пищеварительной системы",
        max_length=255,
        blank=True,
        null=True,
    )
    has_oncological_diseases = models.BooleanField(
        "Имеются ли у Вас онкологические заболевания?", default=False
    )
    oncological_diseases = models.CharField(
        "Перечислите имеющиеся онкологические заболевания",
        max_length=255,
        blank=True,
        null=True,
    )
    has_vascular_diseases = models.BooleanField(
        "Имеются ли у Вас заболевания периферических сосудов?", default=False
    )
    vascular_diseases = models.CharField(
        "Перечислите имеющиеся заболевания периферических сосудов",
        max_length=255,
        blank=True,
        null=True,
    )
    has_trauma_or_surgeries = models.BooleanField(
        "Были ли у Вас травмы и хирургические операции?", default=False
    )
    trauma_or_surgeries = models.CharField(
        "Перечислите травмы и хирургические операции и время их происшествия",
        max_length=255,
        blank=True,
        null=True,
    )
    has_osteoporosis_and_joint_problems = models.BooleanField(
        "Имеются ли у Вас остеопороз, проблемы со спиной и суставами?",
        default=False,
    )
    osteoporosis_and_joint_problems = models.CharField(
        "Перечислите имеющиеся проблемы со спиной и суставами",
        max_length=255,
        blank=True,
        null=True,
    )
    has_other_diseases = models.BooleanField(
        "Есть ли у Вас заболевания, не упомянутые в этой анкете?",
        default=False,
    )
    other_diseases = models.TextField(
        "Перечислите имеющиеся заболевания, не упомянутые в этой анкете",
        blank=True,
        null=True,
    )
    use_medications = models.BooleanField(
        "Принимаете ли Вы в настоящее время лекарства?", default=False
    )
    medications = models.TextField(
        "Перечислите принимаемые лекарства", blank=True, null=True
    )
    follow_diet = models.BooleanField("Соблюдаете ли Вы диету?", default=False)
    current_diet = models.CharField(
        "Укажите вашу текущую диету", max_length=255, blank=True, null=True
    )
    is_pregnant = models.BooleanField("Беременны ли Вы?", default=False)
    pregnancy_stage = models.CharField(
        "Срок беременности", max_length=100, blank=True, null=True
    )
    had_birth_in_last_six_months = models.BooleanField(
        "Были ли у Вас роды в последние 6 месяцев?", default=False
    )
    birth_complications = models.TextField(
        "Укажите, были ли осложнения до, во время и после родов и какие",
        blank=True,
        null=True,
    )

    # 4 Physical activity.
    has_regular_training = models.BooleanField(
        "В течение как минимум последних трех месяцев проводятся регулярные тренировки "
        "длительностью не менее 30 минут в день, интенсивностью не ниже умеренной, "
        "с частотой не менее трех раз в неделю.",
        default=False,
    )
    had_physical_activity = models.BooleanField(
        "Были ли у Вас в прошлом занятия, связанные с двигательной активностью?",
        default=False,
        help_text="Cпорт, фитнес, танцы, йога и пр.",
    )
    previous_physical_activity = models.TextField(
        "Перечислите какие Вы имели занятия, связанные с двигательной активностью, и когда",
        blank=True,
        null=True,
    )
    current_physical_activity = models.CharField(
        "Есть ли у Вас в настоящее время занятия, связанные с двигательной активностью ?",
        choices=CurrentPhysicalActivity.choices,
        max_length=1,
    )
    current_physical_activity_period = models.CharField(
        "Cтаж занятий текущей активностью",
        max_length=100,
        blank=True,
        null=True,
    )
    has_signs_of_underrecovery_or_overtraining = models.BooleanField(
        "Имеются ли признаки, которые позволяют заподозрить недовосстановление или перетренированность?",
        default=False,
        help_text="Например, длительная усталость/ощущение утренней разбитости после тренировок, "
        "снижение работоспособности, раздражительность или перепады настроения, "
        "сильное нежелание тренироваться, нарушения сна.",
    )
    signs_of_underrecovery_or_overtraining = models.TextField(
        "Перечислите признаки недовосстановления или перетренированности",
        blank=True,
        null=True,
    )

    # 5 Other issues and individual requirements.
    has_work_rest_schedule_issues = models.BooleanField(
        "Имеются ли особенности режима работы и отдыха, которые могут повлиять на переносимость нагрузок "
        "и восстановление после них?",
        default=False,
        help_text="Например, сменный или ненормированный рабочий день, частые авралы на работе, "
        "невозможность полноценного сна, проблемы с регулярным питанием и пр.",
    )
    work_rest_schedule_issues = models.TextField(
        "Перечислите имеющиеся особенности режима работы и отдыха, которые могут повлиять на "
        "переносимость нагрузок и восстановление",
        blank=True,
        null=True,
    )
    has_other_issues = models.BooleanField(
        "Имеются ли не отраженные в анкете моменты, которые могут вызвать трудности "
        "при проведении тренировок/тестов на физическую подготовленность?",
        default=False,
    )
    other_issues = models.TextField(
        "Перечислите остальные моменты, которые могут вызвать трудности "
        "при проведении тренировок/тестов на физическую подготовленность",
        blank=True,
        null=True,
    )

    # Result
    is_filled = models.BooleanField("Анкета заполнена", default=False)
    workout_readiness = models.CharField(
        "Готовность к нагрузкам",
        max_length=1,
        choices=WorkoutReadiness.choices,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Информация о здоровье: {self.client}"

    class Meta:
        verbose_name = "Информация о здоровье"
        verbose_name_plural = "Информация о здоровье"


class Contacts(models.Model):
    """Contacts of the client"""

    class Messengers(models.TextChoices):
        EMAIL = "EM", "Email"
        TELEGRAM = "TG", "Telegram"
        WHATSAPP = "WA", "Whatsapp"
        DISCORD = "DC", "Discord"
        SKYPE = "SK", "Skype"
        VK = "VK", "Vkontakte"
        FB = "FB", "Facebook"

    telegram = models.URLField(
        "Telegram",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: https://t.me/demmenty",
    )
    whatsapp = models.URLField(
        "Whatsapp",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: https://wa.me/79603280691",
    )
    discord = models.CharField(
        "Discord",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: Demmenty#5187",
    )
    skype = models.URLField(
        "Skype",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: join.skype.com/invite/ANfPTptWeOxA",
    )
    vkontakte = models.URLField(
        "Vkontakte",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: https://vk.com/id93683216",
    )
    facebook = models.URLField(
        "Facebook",
        max_length=250,
        null=True,
        blank=True,
        help_text="Пример: https://www.facebook.com/parabola.parabola.963",
    )
    preferred_contact = models.CharField(
        "Предпочтительный способ связи",
        choices=Messengers.choices,
        blank=True,
        null=True,
        max_length=2,
    )
    client = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, verbose_name="Клиент"
    )

    def __str__(self):
        return f"Контакты: {self.client}"

    class Meta:
        verbose_name = "Контакты клиента"
        verbose_name_plural = "Контакты клиентов"


class Log(models.Model):
    """Change log of the client's information"""

    action_time = models.DateField("Дата изменения", default=now, editable=False)
    modelname = models.CharField("Модель данных", max_length=255)
    description = models.CharField("Описание", max_length=255)
    client = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Клиент"
    )

    def __str__(self):
        return f"Изменение №{self.pk}"

    def save(self, *args, **kwargs):
        if len(self.description) > 255:
            self.description = self.description[:252] + "..."

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "История действий"
        verbose_name_plural = "Истории действий"
