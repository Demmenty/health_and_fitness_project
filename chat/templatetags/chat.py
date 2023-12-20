from django import template
from django.db.models import Count

from chat.forms import MessageForm
from chat.models import Message
from chat.utils import get_chat_participants

register = template.Library()


@register.inclusion_tag("chat/chat.html", takes_context=True)
def chat(context, partner_id: int | None = None) -> dict:
    """Renders the chat between client and expert"""

    user, partner = get_chat_participants(context.request, partner_id)

    message_form = MessageForm(initial={"sender": user.id, "recipient": partner.id})

    new_msgs_count = Message.objects.filter(
        sender=partner, recipient=user, seen=False
    ).aggregate(count=Count("id"))["count"]

    data = {
        "partner": partner,
        "message_form": message_form,
        "new_msgs_count": new_msgs_count,
    }
    return data
