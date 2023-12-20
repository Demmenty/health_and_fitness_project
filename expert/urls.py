from django.urls import path

from expert import ajax, views

app_name = "expert"

urlpatterns = [
    path("", views.clients, name="clients"),
    path("consult_requests/", views.consult_requests, name="consult_requests"),
    path("client/new/", views.client_new, name="client_new"),
    path("note/main/save/", ajax.main_note_save, name="main_note_save"),
    path("note/monthly/get/", ajax.monthly_note_get, name="monthly_note_get"),
    path("note/monthly/save/", ajax.monthly_note_save, name="monthly_note_save"),
    path("client/<int:id>/", views.client_profile, name="client_profile"),
    path("client/<int:id>/health/", views.client_health, name="client_health"),
    path("client/<int:id>/contacts/", views.client_contacts, name="client_contacts"),
    path(
        "client/<int:id>/metrics/daily/",
        views.client_daily_metrics,
        name="client_daily_metrics",
    ),
    path(
        "client/<int:id>/metrics/anthropo/",
        views.client_anthropo_metrics,
        name="client_anthropo_metrics",
    ),
    path("metrics/colors/edit/", views.metrics_colors_edit, name="metrics_colors_edit"),
    path("client/<int:id>/nutrition/", views.client_nutrition, name="client_nutrition"),
]
