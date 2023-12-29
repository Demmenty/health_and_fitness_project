from django.urls import path

from expert_recommendations import views

urlpatterns = [
    path(
        "ajax/save_nutrition_recommendation",
        views.save_nutrition_recommendation,
        name="save_nutrition_recommendation",
    ),
    path(
        "ajax/get_nutrition_recommendation",
        views.get_nutrition_recommendation,
        name="get_nutrition_recommendation",
    ),
]
