from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("", views.main, name="main"),
    path(
        "consult-request/save",
        views.save_consult_request,
        name="save_consult_request",
    ),
]
