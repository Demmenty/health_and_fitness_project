from django.urls import path

from . import views

urlpatterns = [
    path(
        "ajax/save_measure_comment/",
        views.save_measure_comment,
        name="save_measure_comment",
    ),
    path(
        "ajax/get_color_settings/",
        views.get_color_settings,
        name="get_color_settings",
    ),
    path(
        "ajax/save_color_settings/",
        views.save_color_settings,
        name="save_color_settings",
    ),
]
