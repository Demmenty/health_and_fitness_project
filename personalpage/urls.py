from django.urls import path
from . import views


urlpatterns = [
    path('', views.personalpage, name='personalpage'),
    path('health_questionary/', views.health_questionary, name='health_questionary'),
    path('measurements/', views.measurements, name='measurements'),
    path('addmeasure/', views.addmeasure, name='addmeasure'),
    path('anthropometry/', views.anthropometry, name='anthropometry'),
    path('mealjournal/', views.mealjournal, name='mealjournal'),
    path('foodbydate/', views.foodbydate, name='foodbydate'),
    path('foodbymonth/', views.foodbymonth, name='foodbymonth'),
    path('training/', views.training, name='training'),
]
