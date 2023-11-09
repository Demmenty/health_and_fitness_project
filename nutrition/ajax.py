from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from home.utils import get_client_from_request
from nutrition.cache import FatsecretCacheManager
from nutrition.fatsecret import FSManager
from nutrition.models import FatSecretEntry


@login_required
@require_http_methods(["GET"])
def get_daily(request, day: str):
    """
    Retrieves the nutrition information for a given date from the FatSecret API.

    Args:
        request (HttpRequest): The HTTP request object.
        day (str): The date for which to retrieve the nutrition information.
            Should be in the format "YYYY-MM-DD".

    Returns:
        JsonResponse: A JSON response containing the nutrition data as a dict.
    """

    client = get_client_from_request(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    entry_data = FatSecretEntry.objects.filter(client=client).first()
    if not entry_data:
        return HttpResponseNotFound("FS не подключен")

    fatsecret = FSManager(entry_data)
    daily_food = fatsecret.get_daily_food(day)
    daily_nutrition = fatsecret.calc_daily_total_nutrition(daily_food)

    return JsonResponse(data=daily_nutrition)


@login_required
@require_http_methods(["GET"])
def get_daily_food(request):
    """
    Retrieves the consumed food a given day from the FatSecret API.
    Food data is grouped by meal category.
    Result includes total amount and total nutrition.

    Args:
        request (HttpRequest): The HTTP request object.
        day (str): The date for which to retrieve the nutrition information.
            Should be in the format "YYYY-MM-DD".

    Returns:
        JsonResponse: A JSON response containing the food data as a dict.
    """
    
    client = get_client_from_request(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    day = request.GET.get("day", date.today())

    entry_data = FatSecretEntry.objects.filter(client=client).first()
    if not entry_data:
        return HttpResponseNotFound("FS не подключен")

    fatsecret = FSManager(entry_data)

    daily_food = fatsecret.get_daily_food(day)
    daily_total = fatsecret.calc_daily_total_nutrition(daily_food)
    daily_amount = fatsecret.calc_daily_total_amount(daily_food)

    data = {
        "meal": daily_food,
        "total_nutrition": daily_total,
        "total_amount": daily_amount,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def get_monthly(request):
    """
    Retrieves the consumed food nutrition a given month from the FatSecret API.
    Nutrition data is grouped by day.
    Result includes average nutrition for the month (excluding today).

    Args:
        request (HttpRequest): The HTTP request object.
        month (str): The month for which to retrieve the nutrition information.
            Should be in the format "YYYY-MM-DD".

    Returns:
        JsonResponse: A JSON response containing the food data as a dict.
    """

    client = get_client_from_request(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    month = request.GET.get("month", date.today())

    entry_data = FatSecretEntry.objects.filter(client=client).first()
    if not entry_data:
        return HttpResponseNotFound("FS не подключен")
    
    fatsecret = FSManager(entry_data)

    monthly_nutrition = fatsecret.get_monthly_nutrition_list(month)
    avg_monthly_nutrition = fatsecret.calc_monthly_avg_nutrition(
        monthly_nutrition, count_today=False
    )

    data = {
        "days": monthly_nutrition,
        "avg": avg_monthly_nutrition,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def save_food_servings(request):
    """
    Saves the food serving data received from the request.
    Helps then FatSecret did not provide metric info for the food serving.

    Args:
        request: The HTTP request object that contains the serving data.

    Returns:
        HttpResponse: The HTTP response object with the ok message.
    """

    food_servings = dict(request.POST)

    fs_cache = FatsecretCacheManager()
    fs_cache.save_serving(food_servings)

    return HttpResponse("ok")
