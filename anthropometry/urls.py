from django.urls import path
from . import views


urlpatterns = [
    path('ajax/photoaccess_change/', views.photoaccess_change, name='photoaccess_change'),
]