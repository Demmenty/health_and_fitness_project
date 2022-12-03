from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('saveConsultationSignup/', views.saveConsultationSignup, name='saveConsultationSignup'),
]