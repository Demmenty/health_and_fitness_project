from django.urls import path

from . import views

urlpatterns = [
    path("ajax/save_contacts/", views.save_contacts, name="save_contacts"),
    path(
        "ajax/save_clientmemo/", views.save_clientmemo, name="save_clientmemo"
    ),
]
