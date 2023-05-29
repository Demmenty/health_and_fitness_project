from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from expert_recommendations.services import *
from common.services import services
from expert_recommendations.services import *
from datetime import datetime
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseServerError,
)
from fatsecret import GeneralError


@login_required
@require_http_methods(["GET"])
def get_briefbydate(request):
    """Возвращает сводку питания клиента за день"""

    briefdate = request.GET.get("briefdate")
    if not briefdate:
        return HttpResponseBadRequest("Необходимо передать briefdate")
    
    try:
        briefdate = datetime.strptime(briefdate, "%Y-%m-%d")
    except ValueError as error:
        return HttpResponseBadRequest(error)
    
    if request.user.is_expert:
        client_id = request.GET.get("client_id")
        if not client_id:
            return HttpResponseBadRequest("Необходимо передать client_id")
    else:
        client_id = request.user.id

    try:
        daily_food = services.fs.daily_food(client_id, briefdate)
    except GeneralError as error:
        return HttpResponseServerError(error)

    data = {
        "daily_food": daily_food,
    }
    return JsonResponse(data, status=200)


@login_required
@require_http_methods(["GET"])
def get_briefbymonth(request):
    """Возвращает сводку питания клиента за месяц"""

    briefmonth = request.GET.get("briefmonth")
    if not briefmonth:
        return HttpResponseBadRequest("Необходимо передать briefmonth")
    
    try:
        briefmonth = datetime.strptime(briefmonth, "%Y-%m-%d")
    except ValueError as error:
        return HttpResponseBadRequest(error)
    
    if request.user.is_expert:
        client_id = request.GET.get("client_id")
        if not client_id:
            return HttpResponseBadRequest("Необходимо передать client_id")
    else:
        client_id = request.user.id

    try:
        monthly_food = services.fs.monthly_food(client_id, briefmonth)
    except GeneralError as error:
        return HttpResponseServerError(error)

    data = {
        "monthly_food": monthly_food,
    }
    return JsonResponse(data, status=200)
