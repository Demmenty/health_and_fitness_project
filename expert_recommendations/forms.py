from django.forms import HiddenInput, ModelForm, NumberInput, Textarea

from .models import NutritionRecommendation


class NutritionRecommendationForm(ModelForm):
    class Meta:
        model = NutritionRecommendation
        fields = [
            "calories",
            "protein",
            "fats",
            "carbohydrates",
            "note",
        ]
        widgets = {
            "calories": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "1",
                    "required": True,
                }
            ),
            "protein": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "1",
                }
            ),
            "fats": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "1",
                }
            ),
            "carbohydrates": NumberInput(
                attrs={
                    "class": "form-control text-center",
                    "min": "1",
                }
            ),
            "note": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "7",
                }
            ),
        }
