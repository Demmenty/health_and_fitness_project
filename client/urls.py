from django.urls import path

from client import views

app_name = "client"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("health/page/<int:page>", views.health, name="health"),
    path("maindata/", views.maindata, name="maindata"),
    path("contacts/", views.contacts, name="contacts"),
    path("metrics/", views.metrics, name="metrics"),
    path("metrics/add/", views.metrics_add, name="metrics_add"),
    path("nutrition/", views.nutrition, name="nutrition"),
    path("link_fatsecret/", views.link_fatsecret, name="link_fatsecret"),
]
