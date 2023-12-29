from datetime import date

from django import template
from django.contrib.auth.models import User

from client_overview.manager import ClientInfoManager
from common.services import services
from measurements.forms import MeasurementForm
from measurements.models import Measurement
from training.models import Training

register = template.Library()

TRAINING_TYPES = {
    "P": "Силовая тренировка",
    "R": "Круговая силовая тренировка",
    "E": "Тренировка выносливости",
    "I": "Интервальная тренировка",
}


@register.inclusion_tag("client_overview/overview_content.html")
def draw_overview_content(client: User, for_expert: bool = False) -> dict:
    """возвращает параметры для рендеринга контента обзорной страницы"""

    today_measure = Measurement.objects.filter(
        date__exact=date.today(), user=client
    ).first()
    fs_connected = services.fs.is_connected(client)
    health_questionary_filled = ClientInfoManager.is_health_questionary_filled(
        client
    )
    meet_questionary_filled = ClientInfoManager.is_meet_questionary_filled(
        client
    )
    contacts_filled = ClientInfoManager.is_contacts_filled(client)
    today_trainings = Training.objects.filter(client=client, date=date.today())
    today_training_types = [
        TRAINING_TYPES[training.training_type] for training in today_trainings
    ]

    data = {
        "client": client,
        "for_expert": for_expert,
        "today_measure": today_measure,
        "fs_connected": fs_connected,
        "health_questionary_filled": health_questionary_filled,
        "meet_questionary_filled": meet_questionary_filled,
        "contacts_filled": contacts_filled,
        "today_training_types": today_training_types,
    }

    if for_expert:
        client_age = ClientInfoManager.get_age_as_string(client)
        client_height = ClientInfoManager.get_height(client)
        date_joined = client.date_joined.date()

        data.update(
            {
                "client_age": client_age,
                "client_height": client_height,
                "date_joined": date_joined,
            }
        )
    else:
        contacts_form = ClientInfoManager.get_contacts_form(client)
        measure_form = MeasurementForm(instance=today_measure)
        fatsecret_connected = services.fs.is_connected(client)

        data.update(
            {
                "contacts_form": contacts_form,
                "measure_form": measure_form,
                "fatsecret_connected": fatsecret_connected,
            }
        )

    return data
