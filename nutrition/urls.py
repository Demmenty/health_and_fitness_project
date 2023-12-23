from django.urls import path

from nutrition import ajax, views

app_name = "nutrition"

urlpatterns = [
    path("", views.nutrition, name="nutrition"),
    path(
        "no_fatsecret/",
        views.no_fatsecret,
        name="no_fatsecret",
    ),
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
        "get_monthly_top_food",
        ajax.get_monthly_top_food,
        name="get_monthly_top_food",
    ),
    path(
        "update_food_servings/",
        ajax.update_food_servings,
        name="update_food_servings",
    ),
    path(
        "recommendations/<int:client_id>/save",
        ajax.save_recommendations,
        name="save_recommendations",
    ),
]
