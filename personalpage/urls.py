from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalpage, name='personalpage'),
    path('addmeasure/', views.addmeasure, name='addmeasure'),
    path('questionary/', views.questionary, name='questionary'),
]