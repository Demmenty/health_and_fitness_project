from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalpage, name='personalpage'),
    path('addmeasure/', views.addmeasure, name='addmeasure'),
    path('questionary/', views.questionary, name='questionary'),
    path('mealjournal/', views.mealjournal, name='mealjournal'),
    path('fatsecretauth/', views.fatsecretauth, name='fatsecretauth'),

    path('foodbydate/', views.foodbydate, name='foodbydate'),
    path('foodbymonth/', views.foodbymonth, name='foodbymonth'),
]