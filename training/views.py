from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from client_info.manager import ClientInfoManager
from expert_remarks.services import get_remark_forms, get_today_commentary

from .forms import (
    EnduranceExerciseReportForm,
    EnduranceTrainingForm,
    ExerciseForm,
    IntervalExerciseReportForm,
    IntervalTrainingForm,
    PowerExerciseReportForm,
    PowerTrainingForm,
    RoundTrainingForm,
)
from .manager import TrainingManager


# TODO сделать классом и переименовать в TrainingView
def training(request):
    """Страница для контроля тренировок"""

    if request.user.is_anonymous:
        return redirect("loginuser")

    if request.user.is_expert:
        # TODO сделать страницу для эксперта
        template = "training/expertpage_training.html"

        client = User.objects.get(id=request.GET["client_id"])
        client_contacts = ClientInfoManager.get_contacts(client)
        client_remark = get_remark_forms(client)
        client_sex = ClientInfoManager.get_sex(client)

        data = {
            "clientname": client.username,
            "client_id": client.id,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
            "client_sex": client_sex,
        }
        return render(request, template, data)

    if not request.user.is_expert:
        template = "training/clientpage_training.html"

        client = request.user
        client_sex = ClientInfoManager.get_sex(client)
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        training_forms = {
            "power": PowerTrainingForm(initial={"client": client}),
            "round": RoundTrainingForm(initial={"client": client}),
            "endurance": EnduranceTrainingForm(initial={"client": client}),
            "interval": IntervalTrainingForm(initial={"client": client}),
        }
        exercise_report_forms = {
            "power": PowerExerciseReportForm(),
            "endurance": EnduranceExerciseReportForm(),
            "interval": IntervalExerciseReportForm(),
        }
        exercise_form = ExerciseForm(initial={"author": client})

        exercises = TrainingManager.get_exercises(client)

        data = {
            "client": client,
            "client_sex": client_sex,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
            "training_forms": training_forms,
            "exercise_report_forms": exercise_report_forms,
            "exercise_form": exercise_form,
            "exercises": exercises,
        }
        return render(request, template, data)
