from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.fatsecretauth, name='fatsecretauth'),
    path('ajax/foodmetricsave/', views.foodmetricsave, name='foodmetricsave'),
    path('ajax/get_monthly_top/', views.get_monthly_top, name='get_monthly_top'),
]
