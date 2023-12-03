from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from expert.decorators import expert_required
from metrics.forms import LevelsForm
from metrics.models import Colors, Levels
from nutrition.forms import RecommendationForm
from nutrition.models import Recommendation
from users.models import User


@login_required
@require_http_methods(["GET"])
def get_сolouring(request):
    """
    Get the data for a colouring the client's metrics:
    parameters levels and colors which were set by the expert.

    Returns:
        JsonResponse: Response containing the data dictionary.
    """

    if request.user.is_expert:
        client = get_object_or_404(User, id=request.GET.get("client"))
    else:
        client = request.user

    colors = Colors.get_colors()
    client_levels = Levels.get_levels_as_dict(client=client)
    if not client_levels:
        return HttpResponseNotFound("Настройки не найдены")

    data = {
        "colors": colors,
        "parameters": client_levels,
    }
    return JsonResponse(data)


@expert_required
@require_http_methods(["POST"])
def save_levels(request, client_id: int):
    """
    Handles the saving of client metrics levels. Experts only.

    Args:
        request: HttpRequest object representing the incoming request.
        client_id: Integer representing the client ID.
    Returns:
        HttpResponse: Response indicating the success or failure of the operation.
    """

    client = get_object_or_404(User, id=client_id)
    form = LevelsForm(request.POST)

    if form.is_valid():
        parameter = form.cleaned_data["parameter"]
        instance = Levels.objects.filter(client=client, parameter=parameter).first()
        form = LevelsForm(request.POST, instance=instance)
        form.instance.client = client
        form.save()
        return HttpResponse(f'Измерения параметра "{parameter}" сохранены')

    return HttpResponseBadRequest("Данные некорректны")


@expert_required
@require_http_methods(["POST"])
def save_nutrition_recommendations(request, client_id: int):
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
