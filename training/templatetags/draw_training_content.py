from django import template
from django.contrib.auth.models import User

from client_info.manager import ClientInfoManager
from training.forms import (
    EnduranceExerciseReportForm,
    EnduranceTrainingForm,
    ExerciseForm,
    IntervalExerciseReportForm,
    IntervalTrainingForm,
    PowerExerciseReportForm,
    PowerTrainingForm,
    RoundTrainingForm,
)
from training.manager import TrainingManager


register = template.Library()


@register.inclusion_tag("training/training_content.html")
def draw_training_content(client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга контента тренировки"""

    client_sex = ClientInfoManager.get_sex(client)

    exercises = TrainingManager.get_exercises(client)

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

    if for_expert:
        expert = User.get_expert()
        exercise_form = ExerciseForm(initial={"author": expert})
    else:
        exercise_form = ExerciseForm(initial={"author": client})

    data = {
        "client": client,
        "client_sex": client_sex,
        "training_forms": training_forms,
        "exercises": exercises,
        "exercise_form": exercise_form,
        "exercise_report_forms": exercise_report_forms,
        "for_expert": for_expert,
    }
    return data
