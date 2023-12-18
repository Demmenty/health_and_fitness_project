from django.forms import (
    CheckboxInput,
    CheckboxSelectMultiple,
    ClearableFileInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
    URLInput,
    inlineformset_factory,
)

from training.models import Exercise, ExerciseRecord, Training


class ImageFileInput(ClearableFileInput):
    template_name = "widgets/image_file_input.html"


class CustomFileInput(ClearableFileInput):
    template_name = "widgets/custom_file_input.html"


class ExerciseForm(ModelForm):
    """Form for physical exercise"""

    class Meta:
        model = Exercise
        fields = (
            "name",
            "type",
            "tools",
            "areas",
            "muscles",
            "description",
            "mistakes",
            "icon",
            "image1",
            "image2",
            "video_url",
            "video",
        )
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "type": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "tools": CheckboxSelectMultiple(),
            "areas": CheckboxSelectMultiple(),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),
            "muscles": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),
            "mistakes": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),
            "icon": ImageFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "image1": ImageFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "image2": ImageFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "video": CustomFileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "прямая ссылка (ютуб, желательно)",
                    "accept": "video/*",
                }
            ),
            "video_url": URLInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class StrengthTrainingForm(ModelForm):
    """Form for training with type "strength" """

    class Meta:
        model = Training
        fields = (
            "date",
            "client",
            "type",
            "tiredness",
            "comment",
        )
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "type": HiddenInput(),
            "tiredness": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class RoundTrainingForm(ModelForm):
    """Form for training with type "round" """

    class Meta:
        model = Training
        fields = (
            "date",
            "client",
            "type",
            "time",
            "pulse_avg",
            "tiredness",
            "comment",
        )
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "type": HiddenInput(),
            "time": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "tiredness": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class EnduranceTrainingForm(ModelForm):
    """Form for training with type "endurance" """

    class Meta:
        model = Training
        fields = (
            "date",
            "client",
            "type",
            "time",
            "pulse_avg",
            "tiredness",
            "comment",
        )
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "type": HiddenInput(),
            "time": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "tiredness": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class IntervalTrainingForm(ModelForm):
    """Form for training with type "interval" """

    class Meta:
        model = Training
        fields = (
            "date",
            "client",
            "type",
            "pulse_max",
            "tiredness",
            "comment",
        )
        widgets = {
            "date": HiddenInput(),
            "client": HiddenInput(),
            "type": HiddenInput(),
            "pulse_max": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "tiredness": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class ExerciseRecordForm(ModelForm):
    class Meta:
        model = ExerciseRecord
        fields = "__all__"
        widgets = {
            "weight": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "repetitions": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "sets": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "load": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "time": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "pulse_avg": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "high_load_time": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "high_load_pulse": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "low_load_time": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "low_load_pulse": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "cycles": NumberInput(
                attrs={
                    "class": "form-control pe-1",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control border-0 border-top rounded-0 rounded-bottom",
                    "rows": 3,
                    "placeholder": "...",
                }
            ),
            "is_done": CheckboxInput(
                attrs={
                    "class": "form-check-input ms-0",
                }
            ),
        }


# Mapping of training type to its form
TRAINING_FORMS = {
    "endurance": EnduranceTrainingForm,
    "strength": StrengthTrainingForm,
    "round": RoundTrainingForm,
    "interval": IntervalTrainingForm,
}

StrengthExerciseRecordFormset = inlineformset_factory(
    parent_model=Training,
    model=ExerciseRecord,
    form=ExerciseRecordForm,
    extra=0,
    fields=("weight", "repetitions", "sets", "load", "comment", "is_done"),
    can_order=True,
    min_num=0,
    max_num=20,
)

EnduranceExerciseRecordFormset = inlineformset_factory(
    parent_model=Training,
    model=ExerciseRecord,
    form=ExerciseRecordForm,
    extra=0,
    fields=("time", "pulse_avg", "comment", "is_done"),
    can_order=True,
    min_num=0,
    max_num=20,
)

IntervalExerciseRecordFormset = inlineformset_factory(
    parent_model=Training,
    model=ExerciseRecord,
    form=ExerciseRecordForm,
    extra=0,
    fields=(
        "high_load_time",
        "high_load_pulse",
        "low_load_time",
        "low_load_pulse",
        "cycles",
        "comment",
        "is_done",
    ),
    can_order=True,
    min_num=0,
    max_num=20,
)


# Mapping of training type to exercise record form
EXERCISE_RECORD_FORMSETS = {
    "endurance": EnduranceExerciseRecordFormset,
    "strength": StrengthExerciseRecordFormset,
    "round": StrengthExerciseRecordFormset,
    "interval": IntervalExerciseRecordFormset,
}
