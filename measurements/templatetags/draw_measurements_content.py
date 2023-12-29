from datetime import date

from django import template
from django.contrib.auth.models import User

from client_overview.manager import ClientInfoManager
from common.utils import get_noun_ending
from expert_recommendations.services import *
from fatsecret_app.services import *
from measurements.services import *
from measurements.utils import *

register = template.Library()


@register.inclusion_tag(
    "measurements/measurements_content.html", takes_context=True
)
def draw_measurements_content(
    context, client: User, for_expert: bool = False
) -> dict:
    """возвращает словарь параметров для рендеринга контента измерений"""

    # TODO переделать все это позорище
    colorsettings_exist = user_has_measeurecolor_settings(client)
    today_measure = Measurement.objects.filter(
        date__exact=date.today(), user=client
    ).first()

    period_chosen = context.request.GET.get("selectperiod")
    if not period_chosen:
        period_chosen = 7
    else:
        period_chosen = int(period_chosen)

    period_measures = get_last_measures(client, days=period_chosen)
    recommend_nutrition = get_nutrition_recommend_form(client)

    data = {
        "client": client,
        "for_expert": for_expert,
        "today_measure": today_measure,
        "period_measures": period_measures,
        "colorsettings_exist": colorsettings_exist,
        "recommend_nutrition": recommend_nutrition,
    }

    if period_measures:
        period_measures_avg = create_avg_for_measures(period_measures)
        period_measure_comment_forms = get_measure_comment_forms(
            period_measures
        )
        period_as_string = f"{period_chosen} {get_noun_ending(period_chosen, 'день', 'дня', 'дней')}"
        need_to_show_pressure = bool(period_measures_avg.get("pressure"))

        data.update(
            {
                "period_measures_avg": period_measures_avg,
                "period_measure_comment_forms": period_measure_comment_forms,
                "period_as_string": period_as_string,
                "need_to_show_pressure": need_to_show_pressure,
            }
        )

    if for_expert:
        colorset_forms = create_colorset_forms(client)
        normal_pressure = ClientInfoManager.get_normal_pressure(client)

        data.update(
            {
                "colorset_forms": colorset_forms,
                "normal_pressure": normal_pressure,
            }
        )
    else:
        measure_form = MeasurementForm(instance=today_measure)
        fatsecret_connected = services.fs.is_connected(client)
        data.update(
            {
                "measure_form": measure_form,
                "fatsecret_connected": fatsecret_connected,
            }
        )

    return data
