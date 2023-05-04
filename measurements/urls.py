from django.urls import path

from measurements import ajax, views


urlpatterns = [
    path("", views.measurementspage, name="measurementspage"),
    path("addmeasure/", views.addmeasurepage, name="addmeasurepage"),
    path("anthropometry/", views.anthropometrypage, name="anthropometrypage"),
    path(
        "ajax/get_measure/",
        ajax.get_measure,
        name="get_measure",
    ),
    path(
        "ajax/save_measure/",
        ajax.save_measure,
        name="save_measure",
    ),
    path(
        "ajax/save_measure_comment/",
        ajax.save_measure_comment,
        name="save_measure_comment",
    ),
    path(
        "ajax/get_color_settings/",
        ajax.get_color_settings,
        name="get_color_settings",
    ),
    path(
        "ajax/save_color_settings/",
        ajax.save_color_settings,
        name="save_color_settings",
    ),
    path(
        "anthropometry/ajax/save_anthropometry/",
        ajax.save_anthropometry,
        name="save_anthropometry",
    ),
    path(
        "anthropometry/ajax/photoaccess_change/",
        ajax.photoaccess_change,
        name="photoaccess_change",
    ),
]
