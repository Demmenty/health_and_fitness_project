from django.urls import path
from . import views

urlpatterns = [
    path('', views.controlpage, name='controlpage'),
    path('clientpage/', views.clientpage, name='clientpage'),
    path('consult_requests/', views.consult_requests, name='consult_requests'),
    path('get_commentary_form/', views.get_commentary_form, name='get_commentary_form'),
    path('save_commentary_form/', views.save_commentary_form, name='save_commentary_form'),
    path('client_questionary/', views.client_questionary, name='client_questionary'),
    path('client_measurements/', views.client_measurements, name='client_measurements'),
    path('color_settings_save/', views.color_settings_save, name='color_settings_save'),
    path('color_settings_send/', views.color_settings_send, name='color_settings_send'),
    path('client_mealjournal/', views.client_mealjournal, name='client_mealjournal'),
    path('client_foodbydate/', views.client_foodbydate, name='client_foodbydate'),
    path('client_foodbymonth/', views.client_foodbymonth, name='client_foodbymonth'),
    path('client_anthropometry/', views.client_anthropometry, name='client_anthropometry'),
]