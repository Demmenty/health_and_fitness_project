from django.core.serializers import serialize
from django.db.models.deletion import ProtectedError
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views import View

from common.mixins import ClientSelfOrExpertAllowedAJAXMixin

from .forms import ExerciseForm, ExerciseReportForm, TrainingForm
from .models import Exercise, ExerciseReport, Training


class TrainingView(ClientSelfOrExpertAllowedAJAXMixin, View):
    """AJAX методы управления тренировками"""

    def get(self, request, method):
        """Получение данных тренировок"""

        handlers = {
            "get_by_date": self._get_trainings_by_date,
            "get_last": self._get_last_training,
            "get_month_types": self._get_month_types,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def post(self, request, method):
        """Изменение данных тренировок"""

        handlers = {
            "save": self._save_training,
            "delete": self._delete_training,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def _get_trainings_by_date(self, request):
        """Возвращает тренировки за день"""

        client_id = request.GET.get("client")
        date = request.GET.get("date")

        if not date:
            return HttpResponseBadRequest("Необходимо поле date")

        trainings = Training.objects.filter(client=client_id, date=date)
        data = serialize("json", trainings)

        return HttpResponse(data, content_type="application/json")

    def _get_last_training(self, request):
        """Возвращает последнюю тренировку"""

        client_id = request.GET.get("client")
        training_type = request.GET.get("training_type")

        if training_type:
            trainings = Training.objects.filter(
                client=client_id, training_type=training_type
            )
        else:
            trainings = Training.objects.filter(client=client_id)

        if not trainings:
            return HttpResponseNotFound("Тренировка не найдена")

        training = trainings.latest("date")
        data = serialize("json", [training])

        return HttpResponse(data, content_type="application/json")

    def _get_month_types(self, request):
        """Возвращает типы тренировок за месяц (для календаря)"""

        client_id = request.GET.get("client")
        month = request.GET.get("month")
        year = request.GET.get("year")

        if not (month and year):
            return HttpResponseBadRequest("Необходимы поля month и year")

        query = Training.objects.filter(
            client=client_id, date__year=year, date__month=month
        ).values_list("date", "training_type")

        data = {}

        for item in query:
            day = item[0].day
            training_type = item[1]

            if data.get(day):
                data[day].append(training_type)
            else:
                data[day] = [training_type]

        return JsonResponse(data, status=200)

    def _save_training(self, request):
        """Сохранение новой тренировки"""

        client_id = request.POST.get("client")
        form = TrainingForm(request.POST)

        if form.is_valid():
            Training.objects.filter(
                client=client_id,
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

    def _delete_training(self, request):
        """Удаляет тренировку из бд"""

        client_id = request.POST.get("client")
        training_id = request.POST.get("training_id")

        if not training_id:
            return HttpResponseBadRequest("Необходим training_id")

        training = Training.objects.filter(
            client=client_id, id=training_id).first()

        if not training:
            return HttpResponseNotFound("Тренировка не найдена")
        
        training.delete()

        return HttpResponse("Тренировка удалена")


class ExercisesView(ClientSelfOrExpertAllowedAJAXMixin, View):
    """AJAX методы управления упражнениями"""

    def get(self, request, method):
        """Получение данных упражнений"""

        handlers = {
            "get_by_id": self._get_exercise_by_id,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def post(self, request, method):
        """Изменение данных упражнений"""

        handlers = {
            "save": self._save_exercise,
            "update": self._update_exercise,
            "delete": self._delete_exercise,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def _get_exercise_by_id(self, request):
        """Получение данных об упражнении"""

        exercise_id = request.GET.get("exercise_id")

        if not exercise_id:
            return HttpResponseBadRequest("Необходим exercise_id")

        exercise = Exercise.objects.filter(id=exercise_id)
        data = serialize("json", exercise)

        return HttpResponse(data, content_type="application/json")

    def _save_exercise(self, request):
        """Сохранение нового упражнения"""

        client_id = request.POST.get("client")
        form = ExerciseForm(request.POST, request.FILES)

        if form.is_valid():
            same_named_exercise = Exercise.objects.filter(
                author=client_id, name=form.cleaned_data["name"]
            )

            if same_named_exercise:
                return HttpResponseBadRequest(
                    "Упражнение с таким названием уже существует"
                )

            exercise = form.save()

            data = {
                "exercise_id": exercise.id,
                "exercise_name": exercise.name,
            }
            return JsonResponse(data, status=200)

        data = {"form_errors": form.errors}
        return JsonResponse(data, status=400)

    def _update_exercise(self, request):
        """Перезапись упражнения"""

        client_id = request.POST.get("client")
        exercise_id = request.POST.get("exercise_id")

        if not exercise_id:
            return HttpResponseBadRequest("Необходим exercise_id")

        form = ExerciseForm(request.POST, request.FILES)

        if form.is_valid():
            instance = Exercise.objects.filter(id=exercise_id).first()
            if not instance:
                return HttpResponseNotFound("Упражнение не найдено")

            if instance.name != form.cleaned_data["name"]:
                same_named_exercise = Exercise.objects.filter(
                    author=client_id, name=form.cleaned_data["name"]
                )
                if same_named_exercise:
                    return HttpResponseBadRequest(
                        "Упражнение с таким названием уже существует"
                    )

            form = ExerciseForm(request.POST, request.FILES, instance=instance)
            exercise: Exercise = form.save()

            data = {
                "exercise_id": exercise.id,
                "exercise_name": exercise.name,
            }
            return JsonResponse(data, status=200)

        data = {"form_errors": form.errors}
        return JsonResponse(data, status=400)

    def _delete_exercise(self, request):
        """Удаление упражнения"""

        exercise_id = request.POST.get("exercise_id")

        if not exercise_id:
            return HttpResponseBadRequest("Необходим exercise_id")

        exercise = Exercise.objects.filter(id=exercise_id).first()
        if not exercise:
            return HttpResponseNotFound("Упражнение не найдено")

        if not request.user.is_expert:
            if not request.user == exercise.author:
                msg = "У вас нет прав на удаление этого упражнения"
                return HttpResponseForbidden(msg)

        try:
            exercise.delete()
        except ProtectedError:
            msg = "Нельзя удалить упражнение, сохраненное в тренировке"
            return HttpResponseForbidden(msg)

        return HttpResponse("Упражнение удалено")


class ExerciseReportsView(ClientSelfOrExpertAllowedAJAXMixin, View):
    """AJAX методы управления отчетами упражнений"""

    def get(self, request, method):
        """Получение отчетов упражнений"""

        handlers = {
            "get_by_training": self._get_reports_by_training,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def post(self, request, method):
        """Изменение отчетов упражнений"""

        handlers = {
            "save": self._save_report,
        }
        handler = handlers[method]

        if not handler:
            return HttpResponseNotAllowed

        return handler(request)

    def _get_reports_by_training(self, request):
        """Получение данных о проведении упражнений за тренировку"""

        training_id = request.GET.get("training_id")

        if not training_id:
            return HttpResponseBadRequest("Необходим training_id")

        exercise_reports = ExerciseReport.objects.filter(training=training_id)

        if not exercise_reports:
            return HttpResponseNotFound("Записи упражнений отсутствуют")

        data = serialize("json", exercise_reports)
        return HttpResponse(data, content_type="application/json")

    def _save_report(self, request):
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
