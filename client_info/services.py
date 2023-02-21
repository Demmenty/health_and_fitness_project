from .models import HealthQuestionary, ClientContact, MeetQuestionary, ClientMemo
from .forms import HealthQuestionaryForm, ClientContactForm, MeetQuestionaryForm, ClientMemoForm
from datetime import date
from common.utils import get_noun_ending
from typing import Optional, Union


# health_questionary
def is_health_questionary_filled_by(user) -> bool:
    """проверяет, заполнил ли клиент анкету здоровья"""

    result = HealthQuestionary.objects.filter(user=user).exists()

    return result


def get_health_questionary_of(user):
    """достает данные анкеты здоровья клиента из БД (либо None)"""

    health_questionary = HealthQuestionary.objects.filter(user=user).first()

    return health_questionary


def get_health_questionary_form_for(user):
    """возвращает форму для заполнения анкеты здоровья клиента"""

    instance = HealthQuestionary.objects.filter(user=user).first()

    if instance:
        health_questionary_form = HealthQuestionaryForm(instance=instance)
    else:
        health_questionary_form = HealthQuestionaryForm()

    return health_questionary_form

   
def get_age_string(user) -> str:
    """возвращает количество полных лет по дню рождения в анкете здоровья
    в формате 'количество + лет\года\год' или 'неизвестно' 
    """

    health_questionary = get_health_questionary_of(user)

    if not health_questionary:
        client_age = 'неизвестно'
    else:
        birthdate = health_questionary.birth_date

        today = date.today()
        age = today.year - birthdate.year
        if (today.month < birthdate.month or
        (today.month == birthdate.month and today.day < birthdate.day)):
            age = age - 1

        client_age = str(age) + ' ' + get_noun_ending(age, 'год', 'года', 'лет')

    return client_age


def get_age_int(user) -> Union[int, None]:
    """возвращает количество полных лет по дню рождения в анкете здоровья"""

    health_questionary = get_health_questionary_of(user)

    if health_questionary:

        birthdate = health_questionary.birth_date

        today = date.today()
        age = today.year - birthdate.year
        if (today.month < birthdate.month or
        (today.month == birthdate.month and today.day < birthdate.day)):
            age = age - 1

        return age


def get_normal_pressure_of(user) -> str:
    """возвращает нормальное давление клиента, указанное им в анкете здоровья"""

    health_questionary = get_health_questionary_of(user)

    if not health_questionary:
        normal_pressure = 'не заполнено'
    elif health_questionary.norm_pressure == 'no':
        normal_pressure = 'не знает'
    else:
        normal_pressure = health_questionary.norm_pressure

    return normal_pressure 


# meet_questionary
def is_meet_questionary_filled_by(user) -> bool:
    """проверяет, заполнил ли клиент анкету здоровья"""

    result = MeetQuestionary.objects.filter(user=user).exists()

    return result


def get_meet_questionary_of(user):
    """достает данные анкеты здоровья клиента из БД (либо None)"""

    meet_questionary = MeetQuestionary.objects.filter(user=user).first()

    return meet_questionary


def get_meet_questionary_form_for(user):
    """возвращает форму для заполнения анкеты здоровья клиента"""

    instance = MeetQuestionary.objects.filter(user=user).first()

    if instance:
        meet_questionary_form = MeetQuestionaryForm(instance=instance)
    else:
        meet_questionary_form = MeetQuestionaryForm()

    return meet_questionary_form


def get_height(user) -> Union[int, None]:
    """возвращает рост клиента по анкете знакомства или None"""

    meet_questionary = MeetQuestionary.objects.filter(user=user).first()

    if meet_questionary:
        height = meet_questionary.height

        return int(height)


# client_memo
def get_clientmemo_form_for(user):
    """возвращает форму для личной заметки клиента"""

    instance, is_created = ClientMemo.objects.get_or_create(client=user)

    clientmemo_form = ClientMemoForm(instance=instance)

    return clientmemo_form


# client_contacts
# оптимизировать
def get_contacts_of(user) -> dict:
    """достает контакты клиента из БД в виде словаря"""

    instance = ClientContact.objects.filter(user=user).first()

    if not instance:
        return {}
    else:
        fields = [
            'telegram',
            'whatsapp',
            'discord',
            'skype',
            'vkontakte',
            'facebook',
        ]
        for field in fields: 
            if getattr(instance, field):
                # если хотя бы одно поле контактов не пустое - делаем словарь и возвращаем
                client_contacts = {}
                for f in fields:
                    client_contacts[f] = getattr(instance, f)
                client_contacts['preferred'] = getattr(instance, 'preferred_contact')
                return client_contacts
        # иначе контакты считаются пустыми
        return {}


def get_contacts_form_for(user):
    """возвращает форму для заполнения контактов клиента"""

    instance = ClientContact.objects.filter(user=user).first()

    if instance:
        contacts_form = ClientContactForm(instance=instance)
    else:
        contacts_form = ClientContactForm()

    return contacts_form


def is_contacts_filled_by(user) -> bool:
    """проверяет, заполнил ли клиент контакты для связи"""

    entry = ClientContact.objects.filter(user=user).first()

    if not entry:
        return False
    else:
        # проверка, что заполнено хотя бы 1 поле
        fields = [
            'telegram',
            'whatsapp',
            'discord',
            'skype',
            'vkontakte',
            'facebook',
        ]
        for field in fields:
            if getattr(entry, field):
                return True

        return False

           




