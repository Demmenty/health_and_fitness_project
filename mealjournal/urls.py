from django.urls import path

from mealjournal import views

urlpatterns = [
    path("", views.mealjournal_page, name="mealjournal_page"),
    path("foodbydate/", views.foodbydate_page, name="foodbydate_page"),
    path("foodbymonth/", views.foodbymonth_page, name="foodbymonth_page"),
]
