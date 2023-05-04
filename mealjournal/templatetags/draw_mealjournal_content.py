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

    if not services.fs.is_connected(client):
        data = {
            "client_not_connected": True,
            "for_expert": for_expert,
        }
        return data
    
    daily_food = services.fs.daily_food(client, datetime.today())
    monthly_food = services.fs.monthly_food(client, datetime.today())

    prods_without_info = {}
    if daily_food.get("without_info"):
        prods_without_info.update(daily_food["without_info"])
    if monthly_food.get("without_info"):
        prods_without_info.update(monthly_food["without_info"])

    # для поля выбора (потом сделать через js)
    previous_month = date.today() + relativedelta(months=-1)
    previous_month = previous_month.strftime("%Y-%m")

    data = {
        "client": client,
        "daily_food": daily_food,
        "monthly_food": monthly_food,
        "prods_without_info": prods_without_info,
        "previous_month": previous_month,
        "for_expert": for_expert,
    }

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
