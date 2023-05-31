from django.forms import ModelForm, NumberInput, Textarea, IntegerField

from .models import NutritionRecommendation


class NutritionRecommendationForm(ModelForm):
    calories = IntegerField(
        min_value=1, max_value=10000,
        widget=NumberInput(
            attrs={
                "class": "form-control text-center",
                "min": "1",
                "required": True,
            }))
    protein = IntegerField(
        min_value=1, max_value=10000, required=False,
        widget=NumberInput(
            attrs={
                "class": "form-control text-center",
                "min": "1",
            }))
    fats = IntegerField(
        min_value=1, max_value=10000, required=False,
        widget=NumberInput(
            attrs={
                "class": "form-control text-center",
                "min": "1",
            }))
    carbohydrates = IntegerField(
        min_value=1, max_value=10000, required=False,
        widget=NumberInput(
            attrs={
                "class": "form-control text-center",
                "min": "1",
            }))
    
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
            "note": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "7",
                }
            ),
        }
