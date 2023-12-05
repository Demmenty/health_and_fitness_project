from django.urls import path

from client import views

app_name = "client"

# TODO metrics/anthropo/edit/

urlpatterns = [
    # profile
    path("", views.profile, name="profile"),
    path("info/", views.info, name="info"),
    path("health/page/<int:page>/", views.health, name="health"),
    path("contacts/", views.contacts, name="contacts"),
    # metrics
    path("metrics/daily/", views.daily_metrics, name="daily_metrics"),
    path("metrics/daily/edit/", views.daily_metrics_edit, name="daily_metrics_edit"),
    path("metrics/anthropo/", views.anthropo_metrics, name="anthropo_metrics"),
    path(
        "metrics/anthropo/new/", views.anthropo_metrics_new, name="anthropo_metrics_new"
    ),
    # nutrition
    path("nutrition/", views.nutrition, name="nutrition"),
    path("link_fatsecret/", views.link_fatsecret, name="link_fatsecret"),
]
