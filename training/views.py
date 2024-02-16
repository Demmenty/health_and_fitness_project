from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from training.forms import EXERCISE_RECORD_FORMSETS, TRAINING_FORMS, ExerciseForm
from training.models import (
    EXERCISE_TYPE_MAP,
    Area,
    Exercise,
    ExerciseRecord,
    Tool,
    Training,
)
from training.utils import redirect_to_training
from users.utils import get_client, get_client_id


@login_required
@require_http_methods(["POST"])
def training_new(request):
    """Create a new training for a client"""

    client = get_client(request)
    day = request.POST.get("day", date.today().isoformat())
    type = request.POST.get("type")

    if not type:
        raise Http404("Тип тренировки не указан")

    training = Training.objects.create(client=client, date=day, type=type)

    return redirect_to_training(training)


@login_required
@require_http_methods(["GET"])
def trainings(request):
    """Render the page with client's trainings for day (default: today)"""

    client_id = get_client_id(request)
    day = request.GET.get("day", date.today().isoformat())

    training_types = Training.Type.choices
    trainings = [
        {
            "form": TRAINING_FORMS[training.type](instance=training),
            "exercise_formset": EXERCISE_RECORD_FORMSETS[training.type](
                instance=training
            ),
        }
        for training in Training.objects.filter(client=client_id, date=day)
    ]

    template = "training/trainings.html"
    data = {
        "day": date.fromisoformat(day),
        "training_types": training_types,
        "trainings": trainings,
    }
    return render(request, template, data)


@login_required
@require_http_methods(["GET", "POST"])
def exercise_select(request, id):
    """
    Displays exercises selection page for a specific training.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the training to select exercises for.
    """

    training = get_object_or_404(Training, id=id)

    if training.client != request.user and not request.user.is_expert:
        return HttpResponseForbidden("Вы не можете редактировать эту тренировку")

    if request.method == "GET":
        allowed_exercise_type = EXERCISE_TYPE_MAP[training.type]
        exercises = Exercise.objects.filter(type=allowed_exercise_type)
        tools = Tool.objects.all()
        areas = Area.objects.all()

        template = "training/exercise_select.html"
        data = {
            "tools": tools,
            "areas": areas,
            "training": training,
            "exercises": exercises,
        }
        return render(request, template, data)

    if request.method == "POST":
        checked_exercise_ids = request.POST.getlist("exercises")

        training.exercises.set(checked_exercise_ids)

        return redirect_to_training(training)


@login_required
@require_http_methods(["GET"])
def copy_previous(request, id):
    """Copies the records from the previous training to the current training"""

    training = get_object_or_404(Training, id=id)

    if training.client != request.user and not request.user.is_expert:
        return HttpResponseForbidden("Вы не можете редактировать эту тренировку")

    previous_training = training.get_previous()
    if previous_training:
        training.copy_records(from_training=previous_training)

    return redirect_to_training(training)


@login_required
@require_http_methods(["GET", "POST"])
def exercise_replace(request, id):
    """
    View function for replacing an exercise in a training.

    Args:
        request: The HTTP request object.
        id: The ID of the exercise record to be replaced.

    Returns:
        GET: A rendered HTML template for selecting another suitable exercise.
        POST: Replaces the exercise in the exercise record (if selected) with same data.
            Redirects to the training page of this record after.
    """

    exercise_record = get_object_or_404(ExerciseRecord, id=id)
    training = exercise_record.training

    if training.client != request.user and not request.user.is_expert:
        return HttpResponseForbidden("Вы не можете редактировать эту тренировку")

    if request.method == "GET":
        allowed_exercise_type = EXERCISE_TYPE_MAP[training.type]
        exercises_for_replace = Exercise.objects.filter(type=allowed_exercise_type)
        tools = Tool.objects.all()
        areas = Area.objects.all()

        template = "training/exercise_replace.html"
        data = {
            "tools": tools,
            "areas": areas,
            "training": training,
            "exercises": exercises_for_replace,
            "exercise_record": exercise_record,
        }
        return render(request, template, data)

    if request.method == "POST":
        exercise_id = request.POST.get("exercise")

        if exercise_id:
            exercise = get_object_or_404(Exercise, id=exercise_id)
            exercise_record.exercise = exercise
            exercise_record.save()

        return redirect_to_training(training)


@login_required
@require_http_methods(["GET"])
def exercise_form(request):
    """View function for the exercise form (new or edit)"""

    id = request.GET.get("id")
    exercise = get_object_or_404(Exercise, id=id) if id else None

    if exercise and (exercise.author != request.user and not request.user.is_expert):
        return HttpResponseForbidden("Вы не можете редактировать это упражнение")

    form = ExerciseForm(instance=exercise)
    area_map = Area.get_map()

    template = "training/exercise_form.html"
    data = {
        "form": form,
        "area_map": area_map,
    }
    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def exercise_detail(request, id):
    """View function for displaying an exercise detail"""

    exercise = get_object_or_404(Exercise, id=id)

    template = "training/exercise_detail.html"
    data = {
        "exercise": exercise,
    }
    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def exercise_stats(request, id):
    """
    View function for displaying an exercise stats for a particular client.
    Available only for strength training type.
    """

    exercise_record = get_object_or_404(ExerciseRecord, id=id)
    client_id = get_client_id(request)
    exercise = exercise_record.exercise

    records = ExerciseRecord.objects.filter(
        exercise=exercise,
        training__type=exercise_record.training.type,
        training__client_id=client_id,
        is_done=True,
    ).order_by("training__date")

    template = "training/exercise_stats.html"
    data = {
        "exercise": exercise,
        "records": records,
    }
    return render(request, template, data)
