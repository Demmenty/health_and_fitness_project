from django.urls import path

from . import views

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("login/", views.loginuser, name="loginuser"),
    path("logout/", views.logoutuser, name="logoutuser"),
]
