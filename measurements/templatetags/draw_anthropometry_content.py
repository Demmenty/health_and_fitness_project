from django import template
from django.contrib.auth.models import User

from expert_recommendations.services import *
from fatsecret_app.services import *
from measurements.forms import AnthropometryForm
from measurements.services import *
from measurements.utils import *

register = template.Library()


@register.inclusion_tag(
    "measurements/anthropometry_content.html", takes_context=True
)
def draw_anthropometry_content(
    context, client: User, for_expert: bool = False
) -> dict:
    """возвращает словарь параметров для рендеринга контента антропометрии"""

    entries = get_anthropo_entries(client)
    show_all_entries = context.request.GET.get("show_all_entries")
    photoaccess_allowed = is_photoaccess_allowed(client)

    data = {
        "client": client,
        "for_expert": for_expert,
        "entries": entries,
        "show_all_entries": show_all_entries,
        "photoaccess_allowed": photoaccess_allowed,
    }

    if not for_expert:
        new_entry_form = AnthropometryForm()
        photoaccess_form = get_anthropo_photoaccess_form(client)

        data.update(
            {
                "new_entry_form": new_entry_form,
                "photoaccess_form": photoaccess_form,
            }
        )

    return data
