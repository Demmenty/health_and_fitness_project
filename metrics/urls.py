from django.urls import path

from metrics import ajax

app_name = "metrics"

urlpatterns = [
    path(
        "daily/colouring/get",
        ajax.get_сolouring,
        name="get_сolouring",
    ),
    path(
        "daily/levels/<int:client_id>/save",
        ajax.save_levels,
        name="save_levels",
    ),
    path(
        "anthropo/photoaccess/edit",
        ajax.edit_photoaccess,
        name="edit_photoaccess",
    ),
]
