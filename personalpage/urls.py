from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalpage, name='personalpage'),
    path('questionary/', views.questionary, name='questionary'),
    path('measurements/', views.measurements, name='measurements'),
    path('measurements/get_color_settings/', views.get_color_settings, name='get_color_settings'),
    path('measurements/get_monthly_top/', views.get_monthly_top, name='get_monthly_top'),
    path('addmeasure/', views.addmeasure, name='addmeasure'),
    path('get_expert_commentary/', views.get_expert_commentary, name='get_expert_commentary'),
    path('get_count_unread/', views.get_count_unread, name='get_count_unread'),
    path('mark_comment_readed/', views.mark_comment_readed, name='mark_comment_readed'),
    path('commentsave/', views.commentsave, name='commentsave'),
    path('mealjournal/', views.mealjournal, name='mealjournal'),
    path('foodbydate/', views.foodbydate, name='foodbydate'),
    path('foodbymonth/', views.foodbymonth, name='foodbymonth'),
    path('foodmetricsave/', views.foodmetricsave, name='foodmetricsave'),
    path('anthropometry/', views.anthropometry, name='anthropometry'),
    path('photoaccess_change/', views.photoaccess_change, name='photoaccess_change'),
]