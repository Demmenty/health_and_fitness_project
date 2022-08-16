from .models import Measurement
from django.forms import ModelForm, NumberInput, TextInput, DateInput, Textarea

class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['feel',
                  'weight',
                  'fat',
                  'pulse',
                  'pressure_upper',
                  'pressure_lower',
                  'comment',
                  'date',
                  'weekday']

        widgets = {
            'feel': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
            }),
            'weight': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '300',
            }),
            'fat': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
            }),
            'pulse': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '300',
            }),
            'pressure_upper': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '300',
            }),
            'pressure_lower': NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '200',
            }),
            'comment': Textarea(attrs={
                'class': 'form-control',
            }),
            'date': DateInput(attrs={
                'class': 'form-control-plaintext',
                'readonly': True,
            }),
            'weekday': TextInput(attrs={
                'class': 'form-control-plaintext',
                'readonly': True,
            }),
        }