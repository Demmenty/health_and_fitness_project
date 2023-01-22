from django.urls import path
from . import views


urlpatterns = [
    path('ajax/get_color_settings/', views.get_color_settings, name='get_color_settings'),
    path('ajax/save_color_settings/', views.save_color_settings, name='save_color_settings'),
    path('ajax/get_monthly_top/', views.get_monthly_top, name='get_monthly_top'),
]