from personalpage.models import MeasureColorField
from django.forms import ModelForm, NumberInput, TextInput, HiddenInput, DateInput, Textarea, SelectDateWidget, CheckboxInput


class MeasureColorFieldForm(ModelForm):
    class Meta:
        model = MeasureColorField
        fields = ['user',
                  'index',
                  'color',
                  'low_limit',
                  'upper_limit',
                ]
        widgets = {
            'user': HiddenInput(),
            'index': HiddenInput(),
            'color': HiddenInput(),
            'low_limit': NumberInput(attrs={
                'class': 'form-control text-center',
                'min': '0',
            }),
            'upper_limit': NumberInput(attrs={
                'class': 'form-control text-center',
                'min': '0',
            }),
        }
