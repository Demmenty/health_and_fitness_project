from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import JsonResponse
from .forms import TrainingForm, ExerciseForm, ExerciseReportForm
from .models import Training, ExerciseReport


def get_trainings(request):
    """Получение данных тренировки за переданный день"""

    date = request.GET.get("date")
    client = request.GET.get("client")

    trainings = Training.objects.filter(client=client, date=date)
    data = serialize("json", trainings)

    return HttpResponse(data, content_type="application/json")


def get_exercise_reports(request):
    """Получение данных о проведении упражнений за тренировку"""

    training_id = request.GET.get("training_id")

    exercise_reports = ExerciseReport.objects.filter(training=training_id)
    data = serialize("json", exercise_reports)

    return HttpResponse(data, content_type="application/json")


def save_exercise(request):
    """Сохранение упражнения"""

    form = ExerciseForm(request.POST, request.FILES)
    if form.is_valid():
        # TODO проверить, что такого названия еще нет
        form.save()
        return JsonResponse({}, status=200)

    return JsonResponse({}, status=400)


def save_training(request):
    """Сохранение новой тренировки"""

    client_id = request.POST.get("client")
    # можно самому клиенту или эксперту
    # TODO вынести в декораторы
    if request.user.id != int(client_id) and not request.user.is_expert:
        return JsonResponse({}, status=403)

    form = TrainingForm(request.POST)

    if form.is_valid():
        client = form.cleaned_data["client"]
        date = form.cleaned_data["date"]
        training_type = form.cleaned_data["training_type"]

        Training.objects.filter(
            client=client, date=date, training_type=training_type
        ).delete()

        training = form.save()

        data = {
            "training_id": training.id,
        }
        return JsonResponse(data, status=200)

    # TODO вернуть ошибки формы
    return JsonResponse({}, status=400)


def save_exercise_report(request):
    """Сохранение записи проведения упражнения"""

    form = ExerciseReportForm(request.POST)
    if form.is_valid():
        exercise_report = form.save()

        data = {
            "exercise_report": exercise_report.id,
        }
        return JsonResponse(data, status=200)
    
    # TODO вернуть ошибки формы
    return JsonResponse({}, status=200)
