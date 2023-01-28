from django.urls import path
from . import views


urlpatterns = [
    path('ajax/save_nutrition_recommendation', views.save_nutrition_recommendation, name='save_nutrition_recommendation'),
]