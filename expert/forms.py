from django.forms import HiddenInput, ModelForm, NumberInput, Select, Textarea

from expert.models import ClientMainNote, ClientMonthlyNote


class ClientMainNoteForm(ModelForm):
    """Form for the expert's main note about a client"""

    class Meta:
        model = ClientMainNote
        fields = "__all__"
        widgets = {
            "client": HiddenInput(),
            "text": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 19,
                }
            ),
        }


class ClientMonthlyNoteForm(ModelForm):
    """Form for the expert's monthly note about a client"""

    class Meta:
        model = ClientMonthlyNote
        fields = "__all__"
        widgets = {
            "client": HiddenInput(),
            "month": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "year": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "general": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 15,
                }
            ),
            "measurements": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 15,
                }
            ),
            "nutrition": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 15,
                }
            ),
            "workout": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 15,
                }
            ),
        }
