from datetime import date

from django.contrib.auth.models import User

from common.utils import get_noun_ending

from client_overview.forms import (
    ClientContactForm,
    ClientMemoForm,
    HealthQuestionaryForm,
    MeetQuestionaryForm,
)
from client_overview.models import (
    ClientContact,
    ClientMemo,
    HealthQuestionary,
    MeetQuestionary,
)


class ClientInfoManager:
    """управление личной информацией, предоставленной клиентом"""

    def get_contacts(user: User) -> dict:
        """достает контакты клиента из БД в виде словаря"""

        instance = ClientContact.objects.filter(user=user).first()

        if not instance:
            return {}

        fields = [
            "telegram",
            "whatsapp",
            "discord",
            "skype",
            "vkontakte",
            "facebook",
        ]
        for field in fields:
            if getattr(instance, field):
                # если хотя бы одно поле контактов не пустое - делаем словарь и возвращаем
                client_contacts = {}
                for f in fields:
                    client_contacts[f] = getattr(instance, f)
                client_contacts["preferred"] = getattr(
                    instance, "preferred_contact"
                )
                return client_contacts
        # иначе контакты считаются пустыми
        return {}

    def get_contacts_form(user: User) -> ClientContactForm:
        """возвращает форму для заполнения контактов клиента"""

        instance = ClientContact.objects.filter(user=user).first()

        if instance:
            contacts_form = ClientContactForm(instance=instance)
        else:
            contacts_form = ClientContactForm()

        return contacts_form

    def is_contacts_filled(user: User) -> bool:
        """проверяет, заполнил ли клиент контакты для связи"""

        entry = ClientContact.objects.filter(user=user).first()

        if not entry:
            return False

        # проверка, что заполнено хотя бы 1 поле
        fields = [
            "telegram",
            "whatsapp",
            "discord",
            "skype",
            "vkontakte",
            "facebook",
        ]
        for field in fields:
            if getattr(entry, field):
                return True

        return False

    def get_height(user: User) -> int | None:
        """возвращает рост клиента по анкете знакомства или None"""

        meet_questionary = MeetQuestionary.objects.filter(user=user).first()

        if meet_questionary:
            height = meet_questionary.height

            return int(height)

    def get_age(user: User) -> int | None:
        """возвращает количество полных лет по дню рождения в анкете здоровья"""

        health_questionary = HealthQuestionary.objects.filter(
            user=user
        ).first()

        if not health_questionary:
            return

        birthdate = health_questionary.birth_date

        today = date.today()
        age = today.year - birthdate.year
        if today.month < birthdate.month or (
            today.month == birthdate.month and today.day < birthdate.day
        ):
            age = age - 1

        return age

    def get_age_as_string(user: User) -> str:
        """возвращает количество полных лет по дню рождения в анкете здоровья
        в формате 'количество + лет\года\год' или 'неизвестно'
        """

        age = ClientInfoManager.get_age(user)

        if not age:
            return "неизвестно"

        age_as_string = (
            str(age) + " " + get_noun_ending(age, "год", "года", "лет")
        )

        return age_as_string

    def get_health_questionary(user: User) -> HealthQuestionary | None:
        """достает данные анкеты здоровья клиента из БД"""

        health_questionary = HealthQuestionary.objects.filter(
            user=user
        ).first()

        return health_questionary

    def is_health_questionary_filled(user: User) -> bool:
        """проверяет, заполнил ли клиент анкету здоровья"""

        result = HealthQuestionary.objects.filter(user=user).exists()

        return result

    def get_health_questionary_form(user: User) -> HealthQuestionaryForm:
        """возвращает форму для заполнения анкеты здоровья клиента"""

        instance = HealthQuestionary.objects.filter(user=user).first()

        if instance:
            health_questionary_form = HealthQuestionaryForm(instance=instance)
        else:
            health_questionary_form = HealthQuestionaryForm()

        return health_questionary_form

    def get_normal_pressure(user: User) -> str:
        """возвращает нормальное давление клиента, указанное им в анкете здоровья"""

        health_questionary = HealthQuestionary.objects.filter(
            user=user
        ).first()

        if not health_questionary:
            return "не заполнено"

        if health_questionary.norm_pressure == "no":
            return "не знает"

        return health_questionary.norm_pressure

    def get_meet_questionary(user: User) -> MeetQuestionary | None:
        """достает данные анкеты здоровья клиента из БД"""

        meet_questionary = MeetQuestionary.objects.filter(user=user).first()

        return meet_questionary

    def is_meet_questionary_filled(user: User) -> bool:
        """проверяет, заполнил ли клиент анкету здоровья"""

        result = MeetQuestionary.objects.filter(user=user).exists()

        return result

    def get_meet_questionary_form(user: User) -> MeetQuestionaryForm:
        """возвращает форму для заполнения анкеты здоровья клиента"""

        instance = MeetQuestionary.objects.filter(user=user).first()

        if instance:
            meet_questionary_form = MeetQuestionaryForm(instance=instance)
        else:
            meet_questionary_form = MeetQuestionaryForm()

        return meet_questionary_form

    def get_sex(user: User) -> str | None:
        """возвращает пол клиента ("M","F","?")"""

        instance = MeetQuestionary.objects.filter(user=user).first()
        if not instance:
            return

        return instance.sex

    def get_clientmemo_form(user: User) -> ClientMemoForm:
        """возвращает форму для личной заметки клиента"""

        instance, is_created = ClientMemo.objects.get_or_create(client=user)

        clientmemo_form = ClientMemoForm(instance=instance)

        return clientmemo_form
