from django.forms import ModelForm, NumberInput, Textarea

from nutrition.models import Recommendation


class RecommendationForm(ModelForm):
    """Form for nutrition recommendations for the client."""

    class Meta:
        model = Recommendation
        fields = (
            "calories",
            "protein",
            "fat",
            "carbohydrate",
            "comment",
        )
        widgets = {
            "calories": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10000",
                }
            ),
            "protein": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10000",
                }
            ),
            "fat": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10000",
                }
            ),
            "carbohydrate": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "0",
                    "max": "10000",
                }
            ),
            "comment": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 11,
                }
            ),
        }
