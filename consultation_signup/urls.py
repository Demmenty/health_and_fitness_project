from django.urls import path
from . import views

urlpatterns = [
    path('ajax/save_consultation_signup/', views.save_consultation_signup, name='save_consultation_signup'),
]
