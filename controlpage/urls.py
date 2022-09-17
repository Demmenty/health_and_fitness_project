from django.urls import path
from . import views

urlpatterns = [
    path('', views.controlpage, name='controlpage'),
    path('clientpage/', views.clientpage, name='clientpage'),
    path('client_questionary/', views.client_questionary, name='client_questionary'),
]