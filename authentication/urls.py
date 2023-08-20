from django.urls import path

from . import views

urlpatterns = [
    path(
        "client_registration/",
        views.client_registration,
        name="client_registration",
    ),
    path("login/", views.loginuser, name="loginuser"),
    path("logout/", views.logoutuser, name="logoutuser"),
]
