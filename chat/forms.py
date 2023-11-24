from django import forms

from chat.models import Message


class MessageForm(forms.ModelForm):
    """Form for sending a chat message"""

    class Meta:
        model = Message
        fields = (
            "sender",
            "recipient",
            "text",
            "image",
            "audio",
        )
        widgets = {
            "sender": forms.HiddenInput(),
            "recipient": forms.HiddenInput(),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Написать сообщение...",
                    "class": "form-control",
                    "rows": 2,
                }
            ),
            "image": forms.ClearableFileInput(),
            "audio": forms.ClearableFileInput(),
        }
