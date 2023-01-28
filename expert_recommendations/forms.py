from django.forms import ModelForm, NumberInput, Textarea, HiddenInput
from .models import NutritionRecommendation


class NutritionRecommendationForm(ModelForm):
    class Meta:
        model = NutritionRecommendation
        fields = [
            'calories',
            'protein',
            'fats',
            'carbohydrates',
            'note',
        ]
        widgets = {
            'calories': NumberInput(attrs={
                'class': 'form-control text-center',
            }),
            'protein': NumberInput(attrs={
                'class': 'form-control text-center',
            }),
            'fats': NumberInput(attrs={
                'class': 'form-control text-center',
            }),
            'carbohydrates': NumberInput(attrs={
                'class': 'form-control text-center',
            }),
            'note': Textarea(attrs={
                'class': 'form-control',
                'rows': "8",
            }),
        }
