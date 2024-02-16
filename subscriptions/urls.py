from django.urls import path

from subscriptions import views

app_name = "subscription"

urlpatterns = [
    path("detail/", views.subscription_detail, name="detail"),
    path("client/<int:client_id>/edit", views.edit_subscription, name="edit"),
    path("plans/", views.plans, name="plans"),
    path("plan/new/", views.new_plan, name="new_plan"),
    path("plan/<int:plan_id>/edit/", views.edit_plan, name="edit_plan"),
    path("plan/<int:plan_id>/delete/", views.delete_plan, name="delete_plan"),
]
