# Generated by Django 4.2.5 on 2023-10-06 08:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChangeLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action_time",
                    models.DateField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Дата изменения",
                    ),
                ),
                ("change_message", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Health",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "palpitation",
                    models.BooleanField(
                        verbose_name="Неприятное ощущение сильного или нерегулярного сердцебиения при нагрузке или в покое"
                    ),
                ),
                (
                    "dyspnea",
                    models.BooleanField(
                        verbose_name="Одышка при небольшой нагрузке или в покое"
                    ),
                ),
                (
                    "fainting",
                    models.BooleanField(
                        verbose_name="Потемнения в глазах, головокружения, обмороки, потеря равновесия"
                    ),
                ),
                (
                    "chest_pain",
                    models.BooleanField(
                        verbose_name="Дискомфорт или боли в груди при нагрузке или в покое; боль в левой половине нижней челюсти, шеи, левой руке"
                    ),
                ),
                (
                    "ankles_swelling",
                    models.BooleanField(verbose_name="Отечность лодыжек"),
                ),
                (
                    "leg_cramps",
                    models.BooleanField(
                        verbose_name="Чувство жжения, боль, судороги в нижних конечностях при ходьбе на малые дистанции"
                    ),
                ),
                (
                    "restriction_reasons",
                    models.BooleanField(
                        verbose_name="Другие известные причины, по которым следует ограничить физическую активность"
                    ),
                ),
                (
                    "heart_attack",
                    models.BooleanField(verbose_name="Инфаркт миокарда"),
                ),
                (
                    "cardiac_surgery",
                    models.BooleanField(
                        verbose_name="Катетеризация сердца, коронарная ангиопластика, операции на сердце, трансплантация сердца"
                    ),
                ),
                (
                    "pacemaker",
                    models.BooleanField(
                        verbose_name="Кардиостимулятор/имплантируемый сердечный дефибриллятор"
                    ),
                ),
                (
                    "arrhythmia",
                    models.BooleanField(
                        verbose_name="Нарушения сердечного ритма"
                    ),
                ),
                (
                    "heart_defect",
                    models.BooleanField(
                        verbose_name="Врожденные пороки сердца, патологии сердечных клапанов, сердечная недостаточность"
                    ),
                ),
                (
                    "diabetes",
                    models.BooleanField(verbose_name="Сахарный диабет"),
                ),
                (
                    "kidney_disease",
                    models.BooleanField(verbose_name="Заболевания почек"),
                ),
                (
                    "known_blood_pressure",
                    models.BooleanField(
                        verbose_name="Знаете ли Вы свое обычное артериальное давление?"
                    ),
                ),
                (
                    "blood_pressure",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Ваше обычное артериальное давление",
                    ),
                ),
                (
                    "has_glucose_changes",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас изменения нормального уровня глюкозы в крови?"
                    ),
                ),
                (
                    "glucose_level",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Укажите свой уровень сахара в крови",
                    ),
                ),
                (
                    "has_urinary_diseases",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас заболевания мочевыделительной системы?"
                    ),
                ),
                (
                    "urinary_diseases",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся заболевания мочевыделительной системы",
                    ),
                ),
                (
                    "has_respiratory_diseases",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас заболевания дыхательной системы?"
                    ),
                ),
                (
                    "respiratory_diseases",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся заболевания дыхательной системы",
                    ),
                ),
                (
                    "has_digestive_diseases",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас заболевания пищеварительной системы?"
                    ),
                ),
                (
                    "digestive_diseases",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся заболевания пищеварительной системы",
                    ),
                ),
                (
                    "has_oncological_diseases",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас онкологические заболевания?"
                    ),
                ),
                (
                    "oncological_diseases",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся онкологические заболевания",
                    ),
                ),
                (
                    "has_vascular_diseases",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас заболевания периферических сосудов?"
                    ),
                ),
                (
                    "vascular_diseases",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся заболевания периферических сосудов",
                    ),
                ),
                (
                    "has_trauma_or_surgeries",
                    models.BooleanField(
                        verbose_name="Были ли у Вас травмы и хирургические операции?"
                    ),
                ),
                (
                    "trauma_or_surgeries",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите травмы и хирургические операции и время их происшествия",
                    ),
                ),
                (
                    "has_osteoporosis_and_joint_problems",
                    models.BooleanField(
                        verbose_name="Имеются ли у Вас остеопороз, проблемы со спиной и суставами?"
                    ),
                ),
                (
                    "osteoporosis_and_joint_problems",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Перечислите имеющиеся проблемы со спиной и суставами",
                    ),
                ),
                (
                    "has_other_diseases",
                    models.BooleanField(
                        verbose_name="Есть ли у Вас заболевания, не упомянутые в этой анкете?"
                    ),
                ),
                (
                    "other_diseases",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите имеющиеся заболевания, не упомянутые в этой анкете",
                    ),
                ),
                (
                    "use_medications",
                    models.BooleanField(
                        verbose_name="Принимаете ли Вы в настоящее время лекарства?"
                    ),
                ),
                (
                    "medications",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите принимаемые лекарства",
                    ),
                ),
                (
                    "follow_diet",
                    models.BooleanField(
                        verbose_name="Соблюдаете ли Вы диету?"
                    ),
                ),
                (
                    "current_diet",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Укажите вашу текущую диету",
                    ),
                ),
                (
                    "is_pregnant",
                    models.BooleanField(verbose_name="Беременны ли Вы?"),
                ),
                (
                    "pregnancy_stage",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Срок беременности",
                    ),
                ),
                (
                    "had_birth_in_last_six_months",
                    models.BooleanField(
                        verbose_name="Были ли у Вас роды в последние 6 месяцев?"
                    ),
                ),
                (
                    "birth_complications",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Укажите, были ли осложнения до, во время и после родов и какие",
                    ),
                ),
                (
                    "has_regular_training",
                    models.BooleanField(
                        verbose_name="В течение как минимум последних трех месяцев проводятся регулярные тренировки длительностью не менее 30 минут в день, интенсивностью не ниже умеренной, с частотой не менее трех раз в неделю"
                    ),
                ),
                (
                    "had_physical_activity",
                    models.BooleanField(
                        verbose_name="Были ли у Вас в прошлом занятия, связанные с двигательной активностью (спорт, фитнес, танцы, йога и пр.)?"
                    ),
                ),
                (
                    "previous_physical_activity",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите какие Вы имели занятия, связанные с двигательной активностью, и когда",
                    ),
                ),
                (
                    "current_physical_activity",
                    models.CharField(
                        choices=[
                            (
                                "H",
                                "3 занятия в неделю или больше, занятия регулярные, нагрузки от значительных до предельных",
                            ),
                            (
                                "M",
                                "2–3 занятия в неделю, занятия достаточно регулярные, нагрузки от умеренных до значительных",
                            ),
                            (
                                "L",
                                "меньше 2 занятий в неделю, занятия нерегулярные, нагрузки от незначительных до умеренных",
                            ),
                            ("N", "Нет занятий"),
                        ],
                        max_length=1,
                        verbose_name="Есть ли у Вас в настоящее время занятия, связанные с двигательной активностью (спорт, фитнес, танцы, йога и пр.)?",
                    ),
                ),
                (
                    "current_physical_activity_period",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Cтаж занятий текущей активности",
                    ),
                ),
                (
                    "has_signs_of_underrecovery_or_overtraining",
                    models.BooleanField(
                        help_text="Например, длительная усталость/ощущение утренней разбитости после тренировок, снижение работоспособности, раздражительность или перепады настроения, сильное нежелание тренироваться, нарушения сна.",
                        verbose_name="Имеются ли признаки, которые позволяют заподозрить недовосстановление или перетренированность?",
                    ),
                ),
                (
                    "signs_of_underrecovery_or_overtraining",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите признаки недовосстановления или перетренированности",
                    ),
                ),
                (
                    "has_work_rest_schedule_issues",
                    models.BooleanField(
                        help_text="Например, сменный или ненормированный рабочий день, частые авралы на работе, невозможность полноценного сна, проблемы с регулярным питанием и пр.",
                        verbose_name="Имеются ли особенности режима работы и отдыха, которые могут повлиять на переносимость нагрузок и восстановление после них?",
                    ),
                ),
                (
                    "work_rest_schedule_issues",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите имеющиеся особенности режима работы и отдыха, которые могут повлиять на переносимость нагрузок и восстановление",
                    ),
                ),
                (
                    "has_other_issues",
                    models.BooleanField(
                        verbose_name="Имеются ли не отраженные в анкете моменты, которые могут вызвать трудности при проведении тренировок/тестов на физическую подготовленность?"
                    ),
                ),
                (
                    "other_issues",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Перечислите остальные моменты, которые могут вызвать трудности при проведении тренировок/тестов на физическую подготовленность",
                    ),
                ),
                (
                    "confirmation",
                    models.BooleanField(
                        default=False,
                        verbose_name="Подверждаю достоверность предоставленных сведений и даю согласие на обработку персональных данных",
                    ),
                ),
            ],
        ),
    ]