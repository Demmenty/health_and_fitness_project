from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from nutrition.cache import FatsecretCacheManager
from nutrition.fatsecret import FSManager
from nutrition.models import FatSecretEntry
from users.models import User


@login_required
@require_http_methods(["GET"])
def get_total_by_day(request, day: str):
    """
    Retrieves the nutrition information for a given date from the FatSecret API.

    Args:
        request (HttpRequest): The HTTP request object.
        day (str): The date for which to retrieve the nutrition information.
            Should be in the format "YYYY-MM-DD".

    Returns:
        JsonResponse: A JSON response containing the nutrition data as a dict.
    """
    # TODO client = get_client(request)
    if request.user.is_expert:
        client = get_object_or_404(User, id=request.GET.get("client"))
    else:
        client = request.user

    # TODO fs_entry_data = get_fs_entry_data(client)
    entry_data = FatSecretEntry.objects.filter(client=client).first()
    if not entry_data:
        return HttpResponseNotFound("FS не подключен")

    fatsecret = FSManager(entry_data)
    nutrition = fatsecret.get_daily_total_nutrition(day)

    return JsonResponse(nutrition)


@login_required
@require_http_methods(["GET"])
def get_food_by_day(request):
    """
    Retrieves the consumed food a given day from the FatSecret API.

    Args:
        request (HttpRequest): The HTTP request object.
        day (str): The date for which to retrieve the nutrition information.
            Should be in the format "YYYY-MM-DD".

    Returns:
        JsonResponse: A JSON response containing the food data as a dict.
    """
    if request.user.is_expert:
        client = get_object_or_404(User, id=request.GET.get("client"))
    else:
        client = request.user

    day = request.GET.get("day", date.today())

    entry_data = FatSecretEntry.objects.filter(client=client).first()
    if not entry_data:
        return HttpResponseNotFound("FS не подключен")

    fatsecret = FSManager(entry_data)
    day_food = fatsecret.get_daily_food(day)

    return JsonResponse(day_food)


@login_required
@require_http_methods(["POST"])
def save_food_metrics(request):
    """
    Saves the food metric data received from the request.

    Args:
        request: The HTTP request object that contains the food metric data.

    Returns:
        HttpResponse: The HTTP response object with the ok message.
    """
    prods_no_metric = dict(request.POST)
    del prods_no_metric["csrfmiddlewaretoken"]

    fs_cache = FatsecretCacheManager()
    fs_cache.save_foodmetric(prods_no_metric)

    return HttpResponse("ok")
