from django.urls import path

from client import views

app_name = "client"

# TODO metrics/anthropo/edit
# TODO separate into daily/new and daily/edit

urlpatterns = [
    path("", views.profile, name="profile"),
    path("health/page/<int:page>", views.health, name="health"),
    path("info/", views.info, name="info"),
    path("contacts/", views.contacts, name="contacts"),
    path("metrics/", views.metrics, name="metrics"),
    path("metrics/add/", views.metrics_add, name="metrics_add"),
    path("metrics/anthropo", views.anthropo_metrics, name="anthropo_metrics"),
    path(
        "metrics/anthropo/new", views.anthropo_metrics_new, name="anthropo_metrics_new"
    ),
    path("nutrition/", views.nutrition, name="nutrition"),
    path("link_fatsecret/", views.link_fatsecret, name="link_fatsecret"),
]
