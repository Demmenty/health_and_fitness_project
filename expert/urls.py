from django.urls import path

from expert import views

app_name = "expert"

urlpatterns = [
    path("", views.clients, name="clients"),
    path("consult_requests", views.consult_requests, name="consult_requests"),
    path(
        "client/new",
        views.client_registration,
        name="client_registration",
    ),
    path("client/<int:client_id>", views.client_profile, name="client_profile"),
    path(
        "client/<int:client_id>/health",
        views.client_health,
        name="client_health",
    ),
    path(
        "client/<int:client_id>/contacts",
        views.client_contacts,
        name="client_contacts",
    ),
    path(
        "client/<int:client_id>/metrics",
        views.client_metrics,
        name="client_metrics",
    ),
    path("metrics/colors", views.metrics_colors, name="metrics_colors"),
    path(
        "client/<int:client_id>/nutrition",
        views.client_nutrition,
        name="client_nutrition",
    ),
]
