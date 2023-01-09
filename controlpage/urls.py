from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.client_mainpage, name='client_mainpage'),
    path('questionary/', views.client_questionary, name='client_questionary'),
    path('measurements/', views.client_measurements, name='client_measurements'),
    path('anthropometry/', views.client_anthropometry, name='client_anthropometry'),
    path('mealjournal/', views.client_mealjournal, name='client_mealjournal'),
    path('foodbydate/', views.client_foodbydate, name='client_foodbydate'),
    path('foodbymonth/', views.client_foodbymonth, name='client_foodbymonth'),
    path('get_commentary_form/', views.get_commentary_form, name='get_commentary_form'),
    path('get_clientnote_form/', views.get_clientnote_form, name='get_clientnote_form'),
    path('save_commentary_form/', views.save_commentary_form, name='save_commentary_form'),
    path('save_clientnote_form/', views.save_clientnote_form, name='save_clientnote_form'),
    path('save_full_clientnote_form/', views.save_full_clientnote_form, name='save_full_clientnote_form'),
    path('color_settings_save/', views.color_settings_save, name='color_settings_save'),
    path('get_color_settings/', views.get_color_settings, name='get_color_settings'),
]