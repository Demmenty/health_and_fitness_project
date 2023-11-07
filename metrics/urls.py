from django.urls import path

from metrics import ajax

app_name = "metrics"

urlpatterns = [
    path(
        "colouring/get",
        ajax.get_сolouring_data,
        name="get_сolouring_data",
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
