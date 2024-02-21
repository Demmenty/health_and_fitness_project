from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("maintenance/", views.maintenance, name="maintenance"),
]
