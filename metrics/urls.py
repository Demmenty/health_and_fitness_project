from django.urls import path

from metrics import ajax, views

app_name = "metrics"

urlpatterns = [
    path("daily/", views.daily, name="daily"),
    path("daily/edit/", views.daily_edit, name="daily_edit"),
    path("colors/", views.colors, name="colors"),
    path("levels_colors/get/", ajax.levels_colors_get, name="levels_colors_get"),
    path("levels/<int:id>/save/", ajax.levels_save, name="levels_save"),
    path("anthropo/", views.anthropo, name="anthropo"),
    path("anthropo/add/", views.anthropo_add, name="anthropo_add"),
    path("anthropo/<int:id>/edit/", views.anthropo_edit, name="anthropo_edit"),
    path("photoaccess/edit/", ajax.photoaccess_edit, name="photoaccess_edit"),
]
