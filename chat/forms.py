from django.forms import ClearableFileInput, HiddenInput, ModelForm, Textarea

from chat.models import Message


class MessageForm(ModelForm):
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
            "sender": HiddenInput(),
            "recipient": HiddenInput(),
            "text": Textarea(
                attrs={
                    "placeholder": "Написать сообщение...",
                    "class": "form-control",
                    "rows": 2,
                }
            ),
            "image": ClearableFileInput(),
            "audio": ClearableFileInput(),
        }
