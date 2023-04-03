from django.forms import (
    CheckboxInput,
    ClearableFileInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
)

from .models import Exercise, ExerciseReport, Training


class ExerciseForm(ModelForm):
    """Форма для описания вида упражнения"""

    class Meta:
        model = Exercise
        fields = "__all__"
        widgets = {
            "author": HiddenInput(),
            "name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "icon": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "exercise_type": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "6",
                }
            ),
            "target_muscles": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "6",
                }
            ),
            "mistakes": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "6",
                }
            ),
            "effect_areas": HiddenInput(),
            "photo_init_pose": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "photo_work_pose": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "video": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "прямая ссылка (желательно ютуб)",
                }
            ),
        }


class TrainingForm(ModelForm):
    """Общая форма описания тренировки"""

    class Meta:
        model = Training
        fields = "__all__"


class PowerTrainingForm(ModelForm):
    """Форма описания силовой тренировки"""

    class Meta:
        model = Training
        fields = [
            "date",
            "client",
            "training_type",
            "tiredness_due",
            "tiredness_get",
            "comment",
        ]
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "training_type": HiddenInput(
                attrs={
                    "value": "P",
                }
            ),
            "tiredness_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "tiredness_get": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class RoundTrainingForm(ModelForm):
    """Форма описания круговой силовой тренировки"""

    class Meta:
        model = Training
        fields = [
            "date",
            "client",
            "training_type",
            "tiredness_due",
            "tiredness_get",
            "comment",
            "minutes",
            "pulse_avg",
        ]
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "training_type": HiddenInput(
                attrs={
                    "value": "R",
                }
            ),
            "tiredness_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "tiredness_get": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "minutes": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
        }


class EnduranceTrainingForm(ModelForm):
    """Форма описания тренировки на выносливость"""

    class Meta:
        model = Training
        fields = [
            "date",
            "client",
            "training_type",
            "tiredness_due",
            "tiredness_get",
            "comment",
            "minutes",
            "pulse_avg",
        ]
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "training_type": HiddenInput(
                attrs={
                    "value": "E",
                }
            ),
            "tiredness_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "tiredness_get": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "minutes": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
        }


class IntervalTrainingForm(ModelForm):
    """Форма описания интервальной тренировки на выносливость"""

    class Meta:
        model = Training
        fields = [
            "date",
            "client",
            "training_type",
            "tiredness_due",
            "tiredness_get",
            "comment",
            "minutes",
            "pulse_max",
        ]
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "training_type": HiddenInput(
                attrs={
                    "value": "I",
                }
            ),
            "tiredness_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "tiredness_get": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "minutes": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "pulse_max": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
        }


class ExerciseReportForm(ModelForm):
    """Общая форма описания проведения упражнения"""

    class Meta:
        model = ExerciseReport
        fields = "__all__"


class PowerExerciseReportForm(ModelForm):
    """Общая форма описания проведения упражнения на силовой тренировке"""

    class Meta:
        model = ExerciseReport
        fields = [
            "exercise",
            "training",
            "weight",
            "approaches_due",
            "approaches_made",
            "repeats_due",
            "repeats_made",
            "load_due",
            "load_get",
            "is_done",
        ]
        widgets = {
            "exercise": HiddenInput(),
            "training": HiddenInput(),
            "weight": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "approaches_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "approaches_made": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "repeats_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "repeats_made": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "load_due": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "load_get": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "is_done": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class EnduranceExerciseReportForm(ModelForm):
    """Общая форма описания проведения упражнения на тренировке выносливости"""

    class Meta:
        model = ExerciseReport
        fields = [
            "exercise",
            "training",
            "minutes",
            "pulse_avg",
            "is_done",
        ]
        widgets = {
            "exercise": HiddenInput(),
            "training": HiddenInput(),
            "minutes": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "is_done": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class IntervalExerciseReportForm(ModelForm):
    """Общая форма описания проведения упражнения
    на интервальной тренировке выносливости"""

    class Meta:
        model = ExerciseReport
        fields = [
            "exercise",
            "training",
            "high_load_time",
            "high_load_pulse",
            "low_load_time",
            "low_load_pulse",
            "cycles",
            "is_done",
        ]
        widgets = {
            "exercise": HiddenInput(),
            "training": HiddenInput(),
            "high_load_time": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "high_load_pulse": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "low_load_time": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "low_load_pulse": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "cycles": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "is_done": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }