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
        "ajax/delete_training/",
        api.delete_training,
        name="delete_training",
    ),
    path(
        "ajax/get_exercise/",
        api.get_exercise,
        name="get_exercise",
    ),
    path(
        "ajax/save_exercise/",
        api.save_exercise,
        name="save_exercise",
    ),
    path(
        "ajax/update_exercise/",
        api.update_exercise,
        name="update_exercise",
    ),
    path(
        "ajax/delete_exercise/",
        api.delete_exercise,
        name="delete_exercise",
    ),
    path(
        "ajax/save_exercise_report/",
        api.save_exercise_report,
        name="save_exercise_report",
    ),
]
