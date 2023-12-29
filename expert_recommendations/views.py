from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.decorators.http import require_http_methods

from .forms import NutritionRecommendationForm
from .models import NutritionRecommendation


@login_required
@require_http_methods(["POST"])
def save_nutrition_recommendation(request):
    """Сохранение рекомендуемых КБЖУ от эксперта через ajax"""

    if not request.user.is_expert:
        return HttpResponseForbidden("Вы не эксперт!")

    form = NutritionRecommendationForm(request.POST)

    if form.is_valid():
        client_id = request.POST.get("client_id")
        client = User.objects.get(id=client_id)

        instance, is_created = NutritionRecommendation.objects.get_or_create(
            user=client
        )
        form = NutritionRecommendationForm(request.POST, instance=instance)
        form.save()

        return HttpResponse("Рекомендации сохранены")
    else:
        return HttpResponseBadRequest("Информация некорректна")


@login_required
@require_http_methods(["GET"])
def get_nutrition_recommendation(request):
    """Получение рекомендуемых КБЖУ от эксперта через ajax"""

    if request.user.is_expert:
        client_id = request.GET.get("client_id")
        if not client_id:
            return HttpResponseBadRequest("Необходимо передать client_id")
    else:
        client_id = request.user.id

    recommendations = NutritionRecommendation.objects.filter(user=client_id)

    data = serialize("json", recommendations)

    return HttpResponse(data, content_type="application/json")
