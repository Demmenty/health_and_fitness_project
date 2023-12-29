from django import template
from django.contrib.auth.models import User

from chat.forms import ChatMessageForm

register = template.Library()


@register.inclusion_tag("chat/draw_personal_chat.html")
def draw_personal_chat(client: User, for_expert: bool = False) -> dict:
    """возвращает словарь параметров для рендеринга чата с клиентом"""

    if for_expert:
        msg_form = ChatMessageForm(
            initial={"sender": User.get_expert(), "receiver": client}
        )
    else:
        msg_form = ChatMessageForm(
            initial={"sender": client, "receiver": User.get_expert()}
        )

    data = {
        "client": client,
        "for_expert": for_expert,
        "msg_form": msg_form,
    }
    return data
