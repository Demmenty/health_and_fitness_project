from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from fatsecret.fatsecret import GeneralError as FatsecretGeneralError

from expert.decorators import expert_required
from nutrition.cache import FSCacheManager
from nutrition.fatsecret import FSManager
from nutrition.forms import RecommendationForm
from nutrition.models import FatSecretEntry, Recommendation
from subscriptions.decorators import require_access
from users.models import User
from users.utils import get_client

fs_cache = FSCacheManager()


@login_required
@require_access(["NUTRITION", "FULL"])
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

    client = get_client(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    client_entry = FatSecretEntry.objects.filter(client=client).first()
    if not client_entry:
        return HttpResponseNotFound("FS не подключен")

    fs = FSManager(client_entry)

    daily_food = fs.get_daily_food(day)
    daily_nutrition = fs.calc_daily_total_nutrition(daily_food)

    return JsonResponse(data=daily_nutrition)


@login_required
@require_access(["NUTRITION", "FULL"])
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

    client = get_client(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    day = request.GET.get("day", date.today())

    client_entry = FatSecretEntry.objects.filter(client=client).first()
    if not client_entry:
        return HttpResponseNotFound("FS не подключен")

    fs = FSManager(client_entry)

    daily_food = fs.get_daily_food(day)
    daily_total = fs.calc_daily_total_nutrition(daily_food)
    daily_amount = fs.calc_daily_total_amount(daily_food)

    data = {
        "meal": daily_food.get("meal"),
        "no_metric": daily_food.get("no_metric"),
        "total_nutrition": daily_total,
        "total_amount": daily_amount,
    }
    return JsonResponse(data)


@login_required
@require_access(["NUTRITION", "FULL"])
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

    client = get_client(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    month = request.GET.get("month", date.today())

    client_entry = FatSecretEntry.objects.filter(client=client).first()
    if not client_entry:
        return HttpResponseNotFound("FS не подключен")

    fs = FSManager(client_entry)

    monthly_nutrition = fs.get_monthly_nutrition_list(month)
    avg_monthly_nutrition = fs.calc_monthly_avg_nutrition(
        monthly_nutrition, count_today=False
    )

    data = {
        "days": monthly_nutrition,
        "avg": avg_monthly_nutrition,
    }
    return JsonResponse(data)


@login_required
@require_access(["NUTRITION", "FULL"])
@require_http_methods(["POST"])
def update_food_servings(request):
    """
    Updates the food serving metrics received from the request.
    Helps then FatSecret did not provide metric info for the food serving.

    Args:
        request: The HTTP request object that contains the serving data.

    Returns:
        HttpResponse: The HTTP response object with the ok message.
    """

    new_details = dict(request.POST)
    amount_of_details = len(new_details.get("food_id"))

    for i in range(amount_of_details):
        food_id = new_details["food_id"][i]
        serving_id = new_details["serving_id"][i]
        metric_serving_amount = new_details["metric_serving_amount"][i]
        metric_serving_unit = new_details["metric_serving_unit"][i]

        fs_cache.update_food_serving(
            food_id,
            serving_id,
            {
                "metric_serving_amount": metric_serving_amount,
                "metric_serving_unit": metric_serving_unit,
            },
        )

    return HttpResponse("ok")


@login_required
@require_access(["NUTRITION", "FULL"])
@require_http_methods(["GET"])
def get_monthly_top_food(request):
    """
    Get the monthly top food for a client.

    Args:
        request: The HTTP request object.

    Returns:
       JsonResponse: A JSON response containing the top food items for the month.
    """

    client = get_client(request)
    if not client:
        return HttpResponseNotFound("Клиент не найден")

    month = request.GET.get("month", date.today())

    client_entry = FatSecretEntry.objects.filter(client=client).first()
    if not client_entry:
        return HttpResponseNotFound("FS не подключен")

    fs = FSManager(client_entry)

    try:
        monthly_food = fs.get_monthly_food(month)
    except FatsecretGeneralError as e:
        return HttpResponseServerError(str(e))

    top_by_amount = fs.calc_monthly_top(monthly_food, "amount")
    top_by_calories = fs.calc_monthly_top(monthly_food, "calories")

    data = {
        "top_by_amount": top_by_amount,
        "top_by_calories": top_by_calories,
        "no_metric": monthly_food["no_metric"],
    }
    return JsonResponse(data)


@expert_required
@require_http_methods(["POST"])
def save_recommendations(request, client_id: int):
    """
    Save the nutrition recommendations for a client.

    Args:
        client_id (int): The ID of the client.
    """

    client = get_object_or_404(User, id=client_id)
    instance = Recommendation.objects.filter(client=client).first()

    form = RecommendationForm(request.POST, instance=instance)
    if form.is_valid():
        form.instance.client = client
        form.save()
        return HttpResponse("Рекомендации сохранены")

    return HttpResponseBadRequest("Ошибка при сохранении данных")
