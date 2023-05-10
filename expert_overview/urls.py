from django.urls import path
from expert_overview import views, ajax


urlpatterns = [
    path("", views.expert_overview_page, name="expert_overview_page"),
    path(
        "consult_requests_page/",
        views.consult_requests_page,
        name="consult_requests_page",
    ),
    path(
        "ajax/save_consultation_signup/",
        ajax.save_consultation_signup,
        name="save_consultation_signup",
    ),
]
