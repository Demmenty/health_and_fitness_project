from django.urls import path

from client import ajax, views

app_name = "client"

# TODO metrics/anthropo/edit/

urlpatterns = [
    path("", views.profile, name="profile"),
    path("info/", views.info, name="info"),
    path("note/save/", ajax.note_save, name="note_save"),
    path("health/page/<int:page>/", views.health, name="health"),
    path("contacts/", views.contacts, name="contacts"),
    path("metrics/daily/", views.daily_metrics, name="daily_metrics"),
    path("metrics/daily/edit/", views.daily_metrics_edit, name="daily_metrics_edit"),
    path("metrics/anthropo/", views.anthropo_metrics, name="anthropo_metrics"),
    path(
        "metrics/anthropo/new/", views.anthropo_metrics_new, name="anthropo_metrics_new"
    ),
    path("nutrition/", views.nutrition, name="nutrition"),
    path("link_fatsecret/", views.link_fatsecret, name="link_fatsecret"),
]
