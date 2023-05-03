from django import template
from django.contrib.auth.models import User
from common.services import services
from expert_recommendations.services import *
from dateutil.relativedelta import relativedelta
from datetime import datetime


register = template.Library()


@register.inclusion_tag("mealjournal/foodbymonth_content.html", takes_context=True)
def draw_foodbymonth_content(context, client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга питания за месяц"""

    month_str = context.request.GET.get("month")
    month_datetime = datetime.strptime(month_str, "%Y-%m")

    # для подстановки в html (в js)
    prev_month = month_datetime + relativedelta(months=-1)
    next_month = month_datetime + relativedelta(months=1)
    prev_month = prev_month.strftime("%Y-%m")
    next_month = next_month.strftime("%Y-%m")
    
    monthly_food = services.fs.monthly_food(client, month_datetime)

    data = {
        "client": client,
        "briefmonth": month_datetime,
        "prev_month": prev_month,
        "next_month": next_month,
        "monthly_food": monthly_food,
        "for_expert": for_expert,
    }

    return data
