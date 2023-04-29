from django.urls import path

from training import ajax, views


urlpatterns = [
    path("", views.training, name="trainingpage"),
    path(
        "ajax/trainings.<slug:method>/",
        ajax.TrainingView.as_view(),
        name="trainings",
    ),
    path(
        "ajax/exercises.<slug:method>/",
        ajax.ExercisesView.as_view(),
        name="exercises",
    ),
    path(
        "ajax/exercise_reports.<slug:method>/",
        ajax.ExerciseReportsView.as_view(),
        name="exercise_reports",
    ),
]
