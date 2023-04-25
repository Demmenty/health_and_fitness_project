from .forms import NutritionRecommendationForm
from .models import NutritionRecommendation


def get_nutrition_recommend(client):
    """возвращает рекомендации КБЖУ для клиента из БД"""

    instance = NutritionRecommendation.objects.filter(user=client).first()

    return instance


def get_nutrition_recommend_form(client):
    """возвращает форму для рекомендаций КБЖУ"""

    instance = NutritionRecommendation.objects.filter(user=client).first()

    if instance:
        form = NutritionRecommendationForm(instance=instance)
    else:
        form = NutritionRecommendationForm()

    return form
