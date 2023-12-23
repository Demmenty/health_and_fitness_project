from django.urls import path

from client import ajax, views

app_name = "client"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("health/page/<int:page>/", views.health, name="health"),
    path("contacts/", views.contacts, name="contacts"),
    path("note/save/", ajax.note_save, name="note_save"),
]
