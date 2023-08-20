from django.forms import ClearableFileInput, HiddenInput, ModelForm, Textarea

from chat.models import ChatMessage


class ChatMessageForm(ModelForm):
    """Форма для личного сообщения в чате"""

    class Meta:
        model = ChatMessage
        fields = ("sender", "receiver", "text", "image")
        widgets = {
            "sender": HiddenInput(),
            "receiver": HiddenInput(),
            "text": Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Написать сообщение...",
                }
            ),
            "image": ClearableFileInput(),
            "is_read": HiddenInput(),
        }
