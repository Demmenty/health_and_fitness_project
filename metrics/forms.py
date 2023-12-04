from datetime import date

from django.forms import (
    CheckboxInput,
    ClearableFileInput,
    DateInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    Textarea,
    TextInput,
)

from client.utils import create_log_entry
from metrics.models import (
    Anthropometry,
    AnthropometryPhotoAccess,
    Colors,
    DailyData,
    Levels,
)
from users.models import User


class DailyDataForm(ModelForm):
    """Form for daily data of client's body metrics."""

    class Meta:
        model = DailyData
        fields = (
            "date",
            "feel",
            "weight",
            "fat_percentage",
            "pulse",
            "pressure_upper",
            "pressure_lower",
            "calories",
            "protein",
            "fat",
            "carbohydrate",
            "comment",
        )
        widgets = {
            "date": DateInput(
                attrs={
                    "class": "form-control text-center",
                    "type": "date",
                    "required": True,
                },
                format="%Y-%m-%d",
            ),
            "feel": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10",
                    "placeholder": "ощущения по шкале от 1 до 10",
                }
            ),
            "weight": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "300",
                    "placeholder": "вес в килограммах",
                }
            ),
            "fat_percentage": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "100",
                    "placeholder": "жировая масса в % от массы тела",
                }
            ),
            "pulse": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "300",
                    "placeholder": "среднее значение в покое",
                }
            ),
            "pressure_upper": NumberInput(
                attrs={
                    "class": "form-control d-inline text-center",
                    "min": "0",
                    "max": "300",
                    "placeholder": "систолическое давление",
                }
            ),
            "pressure_lower": NumberInput(
                attrs={
                    "class": "form-control d-inline text-center",
                    "min": "0",
                    "max": "200",
                    "placeholder": "диастолическое давление",
                }
            ),
            "calories": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "protein": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "fat": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "carbohydrate": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                }
            ),
        }

    @classmethod
    def get_form(cls, client: User, metrics_date: date | str) -> ModelForm:
        """
        Retrieves a ModelForm instance based on the given client and metrics date.

        Args:
            client (User): The User object representing the client.
            metrics_date (date|str): The date for which the form is requested.
                If the date is a string, it should be in the format "%Y-%m-%d".
                The date is converted to date type for proper representation on the form page.

        Returns:
            ModelForm: The ModelForm instance retrieved based on the given client and metrics date.
        """

        if isinstance(metrics_date, str):
            metrics_date = date.fromisoformat(metrics_date)

        instance = DailyData.objects.filter(date=metrics_date, client=client).first()
        form = (
            cls(instance=instance) if instance else cls(initial={"date": metrics_date})
        )

        return form

    def is_valid(self) -> bool:
        """
        Return True if the form is valid.
        Also check if pressure_upper and pressure_lower are both filled
        or both empty and metrics date is not in the future.
        """

        pressure_upper = self.data.get("pressure_upper")
        pressure_lower = self.data.get("pressure_lower")
        metrics_date = self.data.get("date")

        if pressure_upper and not pressure_lower:
            self.add_error(
                "pressure_lower",
                "Введите значение диастолического давления или оставьте поля давления пустыми.",
            )

        if pressure_lower and not pressure_upper:
            self.add_error(
                "pressure_upper",
                "Введите значение систолического давления или оставьте поля давления пустыми.",
            )

        if date.fromisoformat(metrics_date) > date.today():
            self.add_error(
                "date",
                "Нельзя вводить данные измерений за будущую дату.",
            )

        return self.is_bound and not self.errors

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry."""

        create_log_entry(
            form=self,
            description=f"Внесены измерения за {self.instance.date}",
            client=self.instance.client,
        )

        super().save(*args, **kwargs)


class ColorsForm(ModelForm):
    """Form for colors for color indication of metrics."""

    class Meta:
        model = Colors
        fields = "__all__"
        widgets = {
            "lvl1": TextInput(
                attrs={
                    "class": "col-6 pointer",
                    "type": "color",
                }
            ),
            "lvl2": TextInput(
                attrs={
                    "class": "col-6 pointer",
                    "type": "color",
                }
            ),
            "lvl3": TextInput(
                attrs={
                    "class": "col-6 pointer",
                    "type": "color",
                }
            ),
            "lvl4": TextInput(
                attrs={
                    "class": "col-6 pointer",
                    "type": "color",
                }
            ),
            "lvl5": TextInput(
                attrs={
                    "class": "col-6 pointer",
                    "type": "color",
                }
            ),
        }


class LevelsForm(ModelForm):
    """Form for Metrics Levels for color indication."""

    class Meta:
        model = Levels
        fields = (
            "parameter",
            "lvl1_min",
            "lvl1_max",
            "lvl2_min",
            "lvl2_max",
            "lvl3_min",
            "lvl3_max",
            "lvl4_min",
            "lvl4_max",
            "lvl5_min",
            "lvl5_max",
        )
        widgets = {
            "parameter": HiddenInput(),
            "lvl1_min": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl1_max": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl2_min": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl2_max": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl3_min": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl3_max": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl4_min": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl4_max": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl5_min": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
            "lvl5_max": NumberInput(
                attrs={
                    "class": "form-control text-center pe-1",
                }
            ),
        }


class AnthropometryForm(ModelForm):
    """Form for adding anthropometry metrics by client"""

    class Meta:
        model = Anthropometry
        fields = (
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
        )
        widgets = {
            "shoulder": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "100",
                }
            ),
            "chest": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "200",
                }
            ),
            "waist": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "200",
                }
            ),
            "belly": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "200",
                }
            ),
            "buttocks": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "200",
                }
            ),
            "hip": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "100",
                }
            ),
            "shin": NumberInput(
                attrs={
                    "class": "form-control text-center",
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
    """Form for changing anthropometry photo access"""

    class Meta:
        model = AnthropometryPhotoAccess
        fields = ("is_allowed",)
        widgets = {
            "is_allowed": CheckboxInput(
                attrs={
                    "class": "form-check-input ms-3",
                }
            ),
        }
