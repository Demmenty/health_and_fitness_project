from django.urls import path

from metrics import ajax

app_name = "metrics"

urlpatterns = [
    path(
        "colouring/get",
        ajax.get_сolouring,
        name="get_сolouring",
    ),
    path(
        "levels/<int:client_id>/save",
        ajax.save_levels,
        name="save_levels",
    ),
    path(
        "nutrition/recommendations/<int:client_id>/save",
        ajax.save_nutrition_recommendations,
        name="save_nutrition_recommendations",
    ),
]
