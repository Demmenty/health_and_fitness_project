from .models import HealthQuestionary, ClientContact
from .forms import HealthQuestionaryForm, ClientContactForm
from datetime import date
from common.utils import get_noun_ending


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

   
def get_age_of(user) -> str:
    """возвращает количество полных лет по дню рождения в анкете здоровья"""

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

        client_age = (str(age) + ' ' + get_noun_ending(age, 'год', 'года', 'лет'))

    return client_age


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

           




