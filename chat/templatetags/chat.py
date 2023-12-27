from django import template

from chat.forms import MessageForm
from chat.models import Message
from users.models import EXPERT, User

register = template.Library()


@register.inclusion_tag("chat/chat_card.html", takes_context=True)
def chat_card(context, partner_id: int | None = None) -> dict:
    """Renders the chat between client and expert"""

    user = context.request.user
    partner = User.objects.get(id=partner_id) if user.is_expert else EXPERT
    message_form = MessageForm(initial={"sender": user, "recipient": partner})

    data = {
        "partner": partner,
        "message_form": message_form,
    }
    return data


@register.inclusion_tag("chat/chat_button.html", takes_context=True)
def chat_button(context, partner_id: int | None = None) -> dict:
    """Renders the chat button with the number of new messages"""

    user = context.request.user
    partner_id = partner_id if user.is_expert else EXPERT.id
    new_msgs = Message.objects.filter(sender_id=partner_id, recipient=user, seen=False)

    data = {"new_msgs_count": new_msgs.count()}
    return data
