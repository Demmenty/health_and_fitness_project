from django.urls import path

from . import api, views

urlpatterns = [
    path("", views.training, name="training"),
    path(
        "ajax/get_trainings/",
        api.get_trainings,
        name="get_trainings",
    ),
    path(
        "ajax/get_exercise_reports/",
        api.get_exercise_reports,
        name="get_exercise_reports",
    ),
    path(
        "ajax/save_training/",
        api.save_training,
        name="save_training",
    ),
    path(
        "ajax/save_exercise/",
        api.save_exercise,
        name="save_exercise",
    ),
    path(
        "ajax/save_exercise_report/",
        api.save_exercise_report,
        name="save_exercise_report",
    ),
]
