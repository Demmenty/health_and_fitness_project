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
        "get_daily/<str:day>/",
        ajax.get_daily,
        name="get_daily",
    ),
    path(
        "get_daily_food/",
        ajax.get_daily_food,
        name="get_daily_food",
    ),
    path(
        "get_monthly/",
        ajax.get_monthly,
        name="get_monthly",
    ),
    path(
        "save_food_servings/",
        ajax.save_food_servings,
        name="save_food_servings",
    ),
]
