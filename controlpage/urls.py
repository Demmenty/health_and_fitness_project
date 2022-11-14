from django.urls import path
from . import views

urlpatterns = [
    path('', views.controlpage, name='controlpage'),
    path('clientpage/', views.clientpage, name='clientpage'),
    path('client_questionary/', views.client_questionary, name='client_questionary'),
    path('client_measurements/', views.client_measurements, name='client_measurements'),
    path('color_settings_save/', views.color_settings_save, name='color_settings_save'),
    path('color_settings_send/', views.color_settings_send, name='color_settings_send'),
    path('client_mealjournal/', views.client_mealjournal, name='client_mealjournal'),
    path('client_foodbydate/', views.client_foodbydate, name='client_foodbydate'),
    path('client_foodbymonth/', views.client_foodbymonth, name='client_foodbymonth'),
    path('client_anthropometry/', views.client_anthropometry, name='client_anthropometry'),
]