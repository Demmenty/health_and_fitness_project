from django.urls import path

from expert import ajax, views

app_name = "expert"

urlpatterns = [
    path("", views.clients, name="clients"),
    path("archived/", views.archived_clients, name="archived_clients"),
    path("client/new/", views.client_new, name="client_new"),
    path("client/<int:id>/", views.client_profile, name="client_profile"),
    path("client/<int:id>/archive", views.client_archive, name="client_archive"),
    path("client/<int:id>/unarchive", views.client_unarchive, name="client_unarchive"),
    path("client/<int:id>/health/", views.client_health, name="client_health"),
    path("client/<int:id>/contacts/", views.client_contacts, name="client_contacts"),
    path("client/<int:id>/nutrition/", views.client_nutrition, name="client_nutrition"),
    path("note/main/save/", ajax.main_note_save, name="main_note_save"),
    path("note/monthly/get/", ajax.monthly_note_get, name="monthly_note_get"),
    path("note/monthly/save/", ajax.monthly_note_save, name="monthly_note_save"),
    path("consult_requests/", views.consult_requests, name="consult_requests"),
]
