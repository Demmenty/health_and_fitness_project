from django import template
from django.contrib.auth.models import User
from common.services import services
from expert_recommendations.services import *
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


register = template.Library()


@register.inclusion_tag("mealjournal/mealjournal_content.html")
def draw_mealjournal_content(client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга контента дневника питания"""

    data = {
        "client": client,
        "for_expert": for_expert,
    }

    if not services.fs.is_connected(client):
        data.update({
            "client_not_connected": True
        })
        return data

    if for_expert:
        recommend_nutrition_form = get_nutrition_recommend_form(client)
        data.update({
            "recommend_nutrition_form": recommend_nutrition_form,
        })
    else:
        recommend_nutrition = get_nutrition_recommend(client)
        data.update({
            "recommend_nutrition": recommend_nutrition,
        })

    return data
