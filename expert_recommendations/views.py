from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import NutritionRecommendationForm
from .models import NutritionRecommendation


def save_nutrition_recommendation(request):
    """Сохранение рекомендуемых КБЖУ от эксперта через ajax"""

    if request.user.username != "Parrabolla":
        return JsonResponse({}, status=403)

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

        data = {"result": "сохранено"}
        return JsonResponse(data, status=200)
    else:
        data = {"result": "Информация некорректна. Попробуйте ещё раз."}
        return JsonResponse(data, status=200)
