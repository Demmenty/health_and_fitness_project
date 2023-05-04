from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from .forms import NutritionRecommendationForm
from .models import NutritionRecommendation


def save_nutrition_recommendation(request):
    """Сохранение рекомендуемых КБЖУ от эксперта через ajax"""

    if not request.user.is_expert:
        return HttpResponseForbidden("Вы не эксперт!")

    # получаем форму из запроса
    form = NutritionRecommendationForm(request.POST)
    # проверяем на корректность
    if form.is_valid():
        # определение клиента
        client_id = request.POST.get("client_id")
        client = User.objects.get(id=client_id)

        # получаем запись из БД с этим числом и перезаписываем или создаем
        instance, is_created = NutritionRecommendation.objects.get_or_create(
            user=client
        )
        form = NutritionRecommendationForm(request.POST, instance=instance)
        form.save()

        return HttpResponse("Рекомендации сохранены")
    else:
        return HttpResponseBadRequest("Информация некорректна")
