from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from chat.forms import MessageForm
from users.models import EXPERT, User


@login_required
@require_http_methods(["GET"])
def chat(request):
    """Renders the separate chat page view"""

    user = request.user
    partner_id = request.GET.get("partner_id")
    partner = get_object_or_404(User, id=partner_id) if user.is_expert else EXPERT

    message_form = MessageForm(initial={"sender": user.id, "recipient": partner.id})

    template = "chat/chat_page.html"
    data = {
        "partner": partner,
        "message_form": message_form,
    }
    return render(request, template, data)
