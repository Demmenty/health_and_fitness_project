from django.urls import path

from mealjournal import views, ajax

urlpatterns = [
    path("", views.mealjournal_page, name="mealjournal_page"),
    path("ajax/get_briefbydate", ajax.get_briefbydate, name="get_briefbydate"),
    path("ajax/get_briefbymonth", ajax.get_briefbymonth, name="get_briefbymonth"),
]
