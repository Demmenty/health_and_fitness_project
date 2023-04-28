from django.urls import path

from . import api, views

urlpatterns = [
    path("", views.training, name="training"),
    path(
        "ajax/get_day_trainings/",
        api.get_day_trainings,
        name="get_day_trainings",
    ),
    path(
        "ajax/get_last_training/",
        api.get_last_training,
        name="get_last_training",
    ),
    path(
        "ajax/get_month_training_types/",
        api.get_month_training_types,
        name="get_month_training_types",
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
