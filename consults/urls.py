from django.urls import path

from consults import ajax

app_name = "consults"


urlpatterns = [
    path("request/add", ajax.add_request, name="add"),
    path("request/<int:id>/edit", ajax.edit_request, name="edit"),
    path("request/<int:id>/set_seen", ajax.set_request_seen, name="set_seen"),
    path("request/<int:id>/delete", ajax.delete_request, name="delete"),
]
