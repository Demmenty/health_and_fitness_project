from django.urls import path

from client import ajax, views

app_name = "client"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("questionnaires/", views.questionnaires, name="questionnaires"),
    path("questionnaires/weight", views.weight, name="weight"),
    path("questionnaires/sleep", views.sleep, name="sleep"),
    path("questionnaires/food", views.food, name="food"),
    path("questionnaires/goal", views.goal, name="goal"),
    path("questionnaires/health/page/<int:page>/", views.health, name="health"),
    path("contacts/", views.contacts, name="contacts"),
    path("note/save/", ajax.note_save, name="note_save"),
    path("feedback/", views.feedback, name="feedback"),
]
