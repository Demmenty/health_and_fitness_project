from personalpage.models import MeasureColorField
from django.forms import ModelForm, NumberInput, TextInput, HiddenInput, DateInput, Textarea, SelectDateWidget, CheckboxInput
from .models import Commentary, ConsultationSignup

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
    """Форма для подачи заявки на консультацию"""
    class Meta:
        model = ConsultationSignup
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

class ConsultationBrowseForm(ModelForm):
    """Форма для просмотра заявки на консультацию"""
    class Meta:
        model = ConsultationSignup
        fields = [
            'name',
            'age',
            'location',
            'email',
            'contacts',
            'is_read',
            'expert_note'
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'age': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'location': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'contacts': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'is_read': HiddenInput(),
            'expert_note': Textarea(attrs={
                'class': 'form-control',
                'rows': "5",
            }),
        }