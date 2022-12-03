from personalpage.models import MeasureColorField
from django.forms import ModelForm, NumberInput, TextInput, HiddenInput, DateInput, Textarea, SelectDateWidget, CheckboxInput
from .models import Commentary, Consultationsignup

class MeasureColorFieldForm(ModelForm):
    class Meta:
        model = MeasureColorField
        fields = [
            'user',
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

class CommentaryForm(ModelForm):
    class Meta:
        model = Commentary
        fields = [
            'date',
            'client',
            'general',
            'measurements',
            'nutrition',
            'workout',
            ]
        widgets = {
            'date': DateInput(attrs={
                'class': 'form-control text-center p-1 transition_common',
                'type': 'date',
                'readonly': False,
            }),
            'client': HiddenInput(),
            'general': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
            }),
            'measurements': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
            }),
            'nutrition': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
            }),
            'workout': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
            }),
        }

class ConsultationsignupForm(ModelForm):
    class Meta:
        model = Consultationsignup
        fields = [
            'name',
            'age',
            'location',
            'email',
            'contacts',
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
            }),
            'age': TextInput(attrs={
                'class': 'form-control',
            }),
            'location': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'contacts': TextInput(attrs={
                'class': 'form-control',
            }),
        }