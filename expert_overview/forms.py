from django import forms

from expert_overview.models import ConsultationSignup


class ConsultationsignupForm(forms.ModelForm):
    """Форма для подачи заявки на консультацию"""

    class Meta:
        model = ConsultationSignup
        fields = [
            "name",
            "age",
            "location",
            "email",
            "contacts",
        ]
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


class ConsultationBrowseForm(forms.ModelForm):
    """Форма для просмотра заявки на консультацию"""

    class Meta:
        model = ConsultationSignup
        fields = [
            "name",
            "age",
            "location",
            "email",
            "contacts",
            "is_read",
            "expert_note",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "age": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "contacts": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "is_read": forms.HiddenInput(),
            "expert_note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                }
            ),
        }
