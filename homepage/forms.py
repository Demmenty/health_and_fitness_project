from django.forms import ModelForm, TextInput
from .models import ConsultationSignup

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
