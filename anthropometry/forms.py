from .models import  Anthropometry, AnthropometryPhotoAccess
from django.forms import ModelForm, NumberInput, DateInput
from django.forms import CheckboxInput, ClearableFileInput


class AnthropometryForm(ModelForm):
    class Meta:
        model = Anthropometry
        fields = [
            'date',
            'shoulder',
            'chest',
            'waist',
            'belly',
            'buttocks',
            'hip',
            'shin',
            'photo_1',
            'photo_2',
            'photo_3',
        ]
        widgets = {
            'date': DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'shoulder': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '100',
            }),
            'chest': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '200',
            }),
            'waist': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '200',
            }),
            'belly': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '200',
            }),
            'buttocks': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '200',
            }),
            'hip': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '100',
            }),
            'shin': NumberInput(attrs={
                'class': 'form-control d-inline',
                'min': '0',
                'max': '100',
            }),
            'photo_1': ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'photo_2': ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'photo_3': ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class AnthropoPhotoAccessForm(ModelForm):
    class Meta:
        model = AnthropometryPhotoAccess
        fields = ['photo_access']
        widgets = {'photo_access': CheckboxInput(attrs={
                'class': 'form-check-input ms-3',
                }),}

