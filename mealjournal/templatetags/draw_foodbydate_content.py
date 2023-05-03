from django import template
from django.contrib.auth.models import User
from common.services import services
from expert_recommendations.services import *
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


register = template.Library()


@register.inclusion_tag("mealjournal/foodbydate_content.html", takes_context=True)
def draw_foodbydate_content(context, client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга питания за день"""

    briefdate = context.request.GET.get("date")
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")

    # для подстановки в html (в js)
    prev_date = briefdate - timedelta(days=1)
    next_date = briefdate + timedelta(days=1)
    prev_date = prev_date.strftime("%Y-%m-%d")
    next_date = next_date.strftime("%Y-%m-%d")

    daily_food = services.fs.daily_food(client, briefdate)
    daily_top = services.fs.daily_top(client, briefdate)

    data = {
        "client": client,
        "briefdate": briefdate,
        "prev_date": prev_date,
        "next_date": next_date,
        "daily_food": daily_food,
        "daily_top": daily_top,
        "for_expert": for_expert,
    }

    return data
