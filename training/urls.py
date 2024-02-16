from django.urls import path

from training import ajax, views

app_name = "training"

urlpatterns = [
    path("", views.trainings, name="trainings"),
    path("new/", views.training_new, name="new"),
    path("<int:id>/save/", ajax.training_save, name="save"),
    path("<int:id>/delete/", ajax.training_delete, name="delete"),
    path("<int:id>/exercise_select/", views.exercise_select, name="exercise_select"),
    path("<int:id>/copy_previous/", views.copy_previous, name="copy_previous"),
    path("get_schedule/<int:year>/<int:month>/", ajax.get_schedule, name="get_schedule"),
    path(
        "exercise/record/<int:id>/replace/",
        views.exercise_replace,
        name="exercise_replace",
    ),
    path("exercise/", views.exercise_form, name="exercise_form"),
    path("exercise/save/", ajax.exercise_save, name="exercise_save"),
    path("exercise/delete/", ajax.exercise_delete, name="exercise_delete"),
    path("exercise/<int:id>/details/", views.exercise_detail, name="exercise_detail"),
    path("exercise/<int:id>/stats/", views.exercise_stats, name="exercise_stats"),
]
