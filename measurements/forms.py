from django.forms import (
    CheckboxInput,
    ClearableFileInput,
    DateInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    Textarea,
)

from measurements.models import (
    Anthropometry,
    AnthropometryPhotoAccess,
    MeasureColorField,
    Measurement,
)


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "date",
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
            "date": DateInput(
                attrs={
                    "class": "form-control text-center",
                    "type": "date",
                }
            ),
            "feel": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                }
            ),
            "weight": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "300",
                }
            ),
            "fat": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "100",
                }
            ),
            "pulse": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "300",
                }
            ),
            "pressure_upper": NumberInput(
                attrs={
                    "class": "form-control d-inline text-center",
                    "min": "0",
                    "max": "300",
                }
            ),
            "pressure_lower": NumberInput(
                attrs={
                    "class": "form-control d-inline text-center",
                    "min": "0",
                    "max": "200",
                }
            ),
            "calories": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "нет данных",
                }
            ),
            "protein": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "нет данных",
                }
            ),
            "fats": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "нет данных",
                }
            ),
            "carbohydrates": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "нет данных",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
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


class AnthropometryForm(ModelForm):
    class Meta:
        model = Anthropometry
        fields = [
            "date",
            "shoulder",
            "chest",
            "waist",
            "belly",
            "buttocks",
            "hip",
            "shin",
            "photo_1",
            "photo_2",
            "photo_3",
        ]
        widgets = {
            "date": DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "shoulder": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "100",
                }
            ),
            "chest": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "200",
                }
            ),
            "waist": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "200",
                }
            ),
            "belly": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "200",
                }
            ),
            "buttocks": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "200",
                }
            ),
            "hip": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "100",
                }
            ),
            "shin": NumberInput(
                attrs={
                    "class": "form-control d-inline",
                    "min": "0",
                    "max": "100",
                }
            ),
            "photo_1": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "photo_2": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "photo_3": ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class AnthropometryPhotoAccessForm(ModelForm):
    class Meta:
        model = AnthropometryPhotoAccess
        fields = ["photo_access"]
        widgets = {
            "photo_access": CheckboxInput(
                attrs={
                    "class": "form-check-input ms-3",
                }
            ),
        }
