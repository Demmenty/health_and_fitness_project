from django.urls import path

from consults import ajax

app_name = "consults"

urlpatterns = [
    path("request/save_new", ajax.save_new, name="save_new"),
    path("request/<int:id>/edit", ajax.edit, name="edit"),
    path("request/<int:id>/set_seen", ajax.set_seen, name="set_seen"),
    path("request/<int:id>/delete", ajax.delete, name="delete"),
]
