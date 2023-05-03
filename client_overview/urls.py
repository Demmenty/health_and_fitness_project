from django.urls import path
from client_overview import views, ajax


urlpatterns = [
    path("", views.overviewpage, name="overviewpage"),
    path("meet_questionary/", views.meet_questionary_page, name="meet_questionary_page"),
    path("health_questionary/", views.health_questionary_page, name="health_questionary_page"),
    path("settings/", views.settings_page, name="settings_page"),
    path("ajax/save_contacts/", ajax.save_contacts, name="save_contacts"),
    path("ajax/save_clientmemo/", ajax.save_clientmemo, name="save_clientmemo"),
]
