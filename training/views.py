from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client_overview.manager import ClientInfoManager
from expert_remarks.services import get_remark_forms, get_today_commentary


@login_required
@require_http_methods(["GET"])
def trainingpage(request):
    """Страница для контроля тренировок"""

    if request.user.is_expert:
        template = "training/expert_training_page.html"

        client = User.objects.get(id=request.GET["client_id"])
        client_contacts = ClientInfoManager.get_contacts(client)
        client_remark = get_remark_forms(client)

        data = {
            "client": client,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
            "for_expert": True,
        }

    if not request.user.is_expert:
        template = "training/client_training_page.html"
        
        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    return render(request, template, data)
