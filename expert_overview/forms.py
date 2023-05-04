from django.forms import HiddenInput, ModelForm, Textarea, TextInput

from consultation_signup.models import ConsultationSignup


class ConsultationBrowseForm(ModelForm):
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
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "age": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "location": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "contacts": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "is_read": HiddenInput(),
            "expert_note": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                }
            ),
        }
