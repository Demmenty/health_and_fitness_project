from datetime import date

from .forms import AnthropometryPhotoAccessForm
from .models import Anthropometry, AnthropometryPhotoAccess


def get_anthropo_entry(user, entry_date: date):
    """возвращает антропометрию из БД за выбранный день"""

    entry = Anthropometry.objects.filter(
        date__exact=entry_date, user=user
    ).first()

    return entry


def get_anthropo_entries(user) -> dict:
    """возвращает словарь из измерений антропометрии клиента
    ключи: 'all', 'first', 'last'
    """

    entries = {}

    all_entries = Anthropometry.objects.filter(user=user)

    if all_entries.exists():
        entries["all"] = all_entries
        entries["first"] = all_entries.earliest()

        if len(all_entries) == 1:
            entries["last"] = ""
        elif len(all_entries) == 2:
            entries["last"] = [all_entries.latest()]
        else:
            entries["last"] = reversed(all_entries[0:3])

    return entries


def get_anthropo_photoaccess_form(user):
    """возвращает форму для галочки о разрешении доступа эксперта к фото"""

    instance, is_created = AnthropometryPhotoAccess.objects.get_or_create(
        user=user
    )

    form = AnthropometryPhotoAccessForm(instance=instance)

    return form


def is_photoaccess_allowed(user) -> bool:
    """проверяет, разрешил ли клиент доступ к своим фото в антропометрии"""

    instance = AnthropometryPhotoAccess.objects.filter(user=user).first()

    if instance:
        result = instance.photo_access
    else:
        result = False

    return result
