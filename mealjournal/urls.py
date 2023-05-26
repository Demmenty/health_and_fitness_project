from django.urls import path

from mealjournal import views, ajax

urlpatterns = [
    path("", views.mealjournal_page, name="mealjournal_page"),
    path("foodbydate/", views.foodbydate_page, name="foodbydate_page"),
    path("foodbymonth/", views.foodbymonth_page, name="foodbymonth_page"),
    path("ajax/get_briefbydate", ajax.get_briefbydate, name="get_briefbydate"),
]
