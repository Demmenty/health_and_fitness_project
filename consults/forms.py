from django import forms

from consults.models import Request


class NewRequestForm(forms.ModelForm):
    """The form for new users to make a consultation request"""

    class Meta:
        model = Request
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


class RequestViewForm(forms.ModelForm):
    """The form for expert to view consultation requests"""

    class Meta:
        model = Request
        fields = "__all__"
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
            "seen": forms.HiddenInput(),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                }
            ),
        }
