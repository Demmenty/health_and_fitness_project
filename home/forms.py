from django import forms

from home.models import ConsultRequest


class ConsultRequestForm(forms.ModelForm):
    """The form for the consultation request from users"""

    class Meta:
        model = ConsultRequest
        fields = (
            "name",
            "age",
            "location",
            "email",
            "contacts",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "age": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "contacts": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
