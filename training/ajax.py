from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from training.forms import EXERCISE_RECORD_FORMSETS, TRAINING_FORMS, ExerciseForm
from training.models import Exercise, Training
from users.utils import get_client_id


@login_required
@require_http_methods(["POST"])
def training_save(request, id):
    """
    Handles the saving of a training.

    Args:
        request: The HTTP request object.
            id: The ID of the training record to be saved.
    """

    training = get_object_or_404(
        Training.objects.prefetch_related("exerciserecord_set"), id=id
    )

    if not training:
        return HttpResponseNotFound("Тренировка не найдена")

    if not request.user.is_expert and training.client != request.user:
        return HttpResponseForbidden("Это не ваша тренировка!")

    form = TRAINING_FORMS[training.type](request.POST, instance=training)
    formset = EXERCISE_RECORD_FORMSETS[training.type](
        request.POST,
        instance=training,
        prefix="exerciserecord_set",
    )

    if form.is_valid() and formset.is_valid():
        form.save()
        for form in formset.ordered_forms:
            form.instance.order = form.cleaned_data["ORDER"]
        formset.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def training_delete(request, id):
    """
    Deletes a training record.

    Args:
        request: The HTTP request object.
        id: The ID of the training record to be deleted.
    """

    training = get_object_or_404(Training, id=id)

    if not request.user.is_expert and training.client != request.user:
        return HttpResponseForbidden("Это не ваша тренировка!")

    training.delete()

    return HttpResponse("ok")


@login_required
@require_http_methods(["GET"])
def get_schedule(request, year: int, month: int):
    """
    Get the schedule of client's trainings for a specific year and month.

    Args:
        request: The HTTP request object.
        year: An integer representing the year.
        month: An integer representing the month.
    """

    client_id = get_client_id(request)

    schedule = Training.get_schedule(client_id, year, month)

    return JsonResponse(schedule, status=200)


@login_required
@require_http_methods(["POST"])
def exercise_save(request):
    """Saves an exercise object"""

    id = request.POST.get("id")

    instance = get_object_or_404(Exercise, id=id) if id else None

    if instance and (instance.author != request.user and not request.user.is_expert):
        return HttpResponseForbidden("Вы не можете редактировать это упражнение")

    form = ExerciseForm(request.POST, request.FILES, instance=instance)

    if form.is_valid():
        if not instance:
            form.instance.author = request.user
        form.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)
