from django import template
from django.contrib.auth.models import User

from common.services import services
from expert_recommendations.services import *

register = template.Library()


@register.inclusion_tag("mealjournal/mealjournal_content.html")
def draw_mealjournal_content(client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга контента дневника питания"""

    if services.fs.is_connected(client):
        recommend_nutrition = get_nutrition_recommend_form(client)
        data = {
            "client": client,
            "for_expert": for_expert,
            "recommend_nutrition": recommend_nutrition,
        }
    else:
        data = {
            "client": client,
            "for_expert": for_expert,
            "client_not_connected": True,
        }

    return data
