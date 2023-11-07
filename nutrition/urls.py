from django.urls import path

from nutrition import ajax, views

app_name = "nutrition"

urlpatterns = [
    path(
        "link_fatsecret/",
        views.link_fatsecret,
        name="link_fatsecret",
    ),
    path(
        "get_total_by_day/<str:day>/",
        ajax.get_total_by_day,
        name="get_total_by_day",
    ),
    path(
        "get_food_by_day/",
        ajax.get_food_by_day,
        name="get_food_by_day",
    ),
    path(
        "save_food_metrics/",
        ajax.save_food_metrics,
        name="save_food_metrics",
    ),
]
