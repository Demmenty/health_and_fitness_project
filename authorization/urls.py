from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
]