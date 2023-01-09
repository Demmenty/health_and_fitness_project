from django.urls import path
from . import views

urlpatterns = [
    path('', views.expertpage, name='expertpage'),
    path('consult_requests_page/', views.consult_requests_page, name='consult_requests_page'),
]
