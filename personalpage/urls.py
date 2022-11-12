from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalpage, name='personalpage'),
    path('questionary/', views.questionary, name='questionary'),
    path('measurements/', views.measurements, name='measurements'),
    path('addmeasure/', views.addmeasure, name='addmeasure'),
    path('commentsave/', views.commentsave, name='commentsave'),
    path('mealjournal/', views.mealjournal, name='mealjournal'),
    path('fatsecretauth/', views.fatsecretauth, name='fatsecretauth'),
    path('foodbydate/', views.foodbydate, name='foodbydate'),
    path('foodbymonth/', views.foodbymonth, name='foodbymonth'),
    path('foodmetricsave/', views.foodmetricsave, name='foodmetricsave'),
    path('anthropometry/', views.anthropometry, name='anthropometry'),
    path('photoaccess_change/', views.photoaccess_change, name='photoaccess_change'),
]