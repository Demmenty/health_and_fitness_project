from django.core.serializers import serialize
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from .forms import ExerciseForm, ExerciseReportForm, TrainingForm
from .models import Exercise, ExerciseReport, Training, User

# TODO сделать classы View


def get_trainings(request):
    """Получение данных тренировки за переданный день"""

    date = request.GET.get("date")
    client = request.GET.get("client")

    trainings = Training.objects.filter(client=client, date=date)
    data = serialize("json", trainings)

    return HttpResponse(data, content_type="application/json")


def get_month_training_types(request):
    """Возвращает типы тренировок за месяц"""

    month = request.GET.get("month")
    year = request.GET.get("year")
    client = request.GET.get("client")

    result = Training.objects.filter(
        client=client, 
        date__year=year, 
        date__month=month).values_list('date', 'training_type')

    data = {}

    for item in result:
        day = item[0].day
        training_type = item[1]

        if data.get(day):
            data[day].append(training_type)
        else:
            data[day] = [training_type]

    return JsonResponse(data, status=200)


def delete_training(request):
    """Удаление тренировки"""

    if request.method == "POST":
        training_id = request.POST.get("training_id")
        training = Training.objects.filter(id=training_id).first()

        if not request.user.is_expert:
            if not request.user == training.client:
                msg = "У вас нет прав на удаление тренировки"
                return HttpResponseForbidden(msg)

        training.delete()

        msg = "Тренировка удалена"
        return HttpResponse(msg)


def get_exercise_reports(request):
    """Получение данных о проведении упражнений за тренировку"""

    training_id = request.GET.get("training_id")

    exercise_reports = ExerciseReport.objects.filter(training=training_id)
    data = serialize("json", exercise_reports)

    return HttpResponse(data, content_type="application/json")


def get_exercise(request):
    """Получение данных о упражнении"""

    exercise_id = request.GET.get("exercise_id")

    exercise = Exercise.objects.filter(id=exercise_id)
    data = serialize("json", exercise)

    return HttpResponse(data, content_type="application/json")


def save_exercise(request):
    """Сохранение нового упражнения"""

    # TODO можно самому клиенту или эксперту - в декораторы

    form = ExerciseForm(request.POST, request.FILES)

    if form.is_valid():
        # TODO проверить, что такого названия еще нет
        exercise = form.save()

        data = {
            "exercise_id": exercise.id,
            "exercise_name": exercise.name,
        }
        return JsonResponse(data, status=200)

    data = {"form_errors": form.errors}
    return JsonResponse(data, status=400)


def update_exercise(request):
    """Перезапись упражнения"""

    exercise_id = request.POST.get("exercise_id")

    form = ExerciseForm(request.POST, request.FILES)

    if form.is_valid():
        instance = Exercise.objects.filter(id=exercise_id).first()
        form = ExerciseForm(request.POST, request.FILES, instance=instance)
        exercise: Exercise = form.save()

        data = {
            "exercise_id": exercise.id,
            "exercise_name": exercise.name,
        }
        return JsonResponse(data, status=200)

    data = {"form_errors": form.errors}
    return JsonResponse(data, status=400)


def delete_exercise(request):
    """Удаление упражнения"""

    if request.method == "POST":
        exercise_id = request.POST.get("exercise_id")
        exercise = Exercise.objects.filter(id=exercise_id).first()

        if not request.user.is_expert:
            if not request.user == exercise.author:
                msg = "У вас нет прав на удаление этого упражнения"
                return HttpResponseForbidden(msg)

        try:
            exercise.delete()
        except ProtectedError:
            msg = "Нельзя удалить упражнение, сохраненное в тренировке"
            return HttpResponseForbidden(msg)

        msg = "Упражнение удалено"
        return HttpResponse(msg)


def save_training(request):
    """Сохранение новой тренировки"""

    client_id = request.POST.get("client")
    # можно самому клиенту или эксперту
    # TODO вынести в декораторы
    if request.user.id != int(client_id) and not request.user.is_expert:
        return JsonResponse({}, status=403)

    form = TrainingForm(request.POST)

    if form.is_valid():
        Training.objects.filter(
            client=form.cleaned_data["client"],
            date=form.cleaned_data["date"],
            training_type=form.cleaned_data["training_type"],
        ).delete()

        training = form.save()

        data = {
            "training_id": training.id,
        }
        return JsonResponse(data, status=200)

    data = {"form_errors": form.errors}
    return JsonResponse(data, status=400)


def save_exercise_report(request):
    """Сохранение записи проведения упражнения"""

    form = ExerciseReportForm(request.POST)
    if form.is_valid():
        exercise_report = form.save()

        data = {
            "exercise_report": exercise_report.id,
        }
        return JsonResponse(data, status=200)

    data = {"form_errors": form.errors}
    return JsonResponse(data, status=400)
