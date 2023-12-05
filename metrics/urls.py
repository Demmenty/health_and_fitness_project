from django.urls import path

from metrics import ajax

app_name = "metrics"

urlpatterns = [
    path("levels_colors/get/", ajax.levels_colors_get, name="levels_colors_get"),
    path("levels/<int:id>/save/", ajax.levels_save, name="levels_save"),
    path("photoaccess/edit/", ajax.photoaccess_edit, name="photoaccess_edit"),
]
