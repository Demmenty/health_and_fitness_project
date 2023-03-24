from django.urls import path

from . import views

urlpatterns = [
    path("main/", views.client_mainpage, name="client_mainpage"),
    path(
        "meet_questionary/",
        views.client_meet_questionary,
        name="client_meet_questionary",
    ),
    path(
        "health_questionary/",
        views.client_health_questionary,
        name="client_health_questionary",
    ),
    path(
        "measurements/", views.client_measurements, name="client_measurements"
    ),
    path(
        "anthropometry/",
        views.client_anthropometry,
        name="client_anthropometry",
    ),
    path("mealjournal/", views.client_mealjournal, name="client_mealjournal"),
    path("foodbydate/", views.client_foodbydate, name="client_foodbydate"),
    path("foodbymonth/", views.client_foodbymonth, name="client_foodbymonth"),
]
