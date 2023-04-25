from django.forms import (
    DateInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    Textarea,
)

from .models import MeasureColorField, Measurement


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "feel",
            "weight",
            "fat",
            "pulse",
            "pressure_upper",
            "pressure_lower",
            "comment",
            "date",
            "calories",
            "protein",
            "fats",
            "carbohydrates",
        ]
        widgets = {
            "feel": NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "weight": NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "300",
                }
            ),
            "fat": NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                }
            ),
            "pulse": NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "300",
                }
            ),
            "pressure_upper": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "300",
                }
            ),
            "pressure_lower": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "200",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                }
            ),
            "date": DateInput(
                attrs={
                    "class": "form-control-plaintext",
                    "readonly": True,
                }
            ),
            "calories": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "нет данных",
                }
            ),
            "protein": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "нет данных",
                }
            ),
            "fats": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "нет данных",
                }
            ),
            "carbohydrates": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "нет данных",
                }
            ),
        }


class MeasurementCommentForm(ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "comment",
            "date",
        ]
        widgets = {
            "date": DateInput(
                attrs={
                    "class": "form-control-plaintext",
                    "type": "hidden",
                    "readonly": True,
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class MeasureColorFieldForm(ModelForm):
    """Форма для настройки цветовых полей таблицы измерений"""

    class Meta:
        model = MeasureColorField
        fields = [
            "user",
            "index",
            "color",
            "low_limit",
            "upper_limit",
        ]
        widgets = {
            "user": HiddenInput(),
            "index": HiddenInput(),
            "color": HiddenInput(),
            "low_limit": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
            "upper_limit": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                }
            ),
        }
