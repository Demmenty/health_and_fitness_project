from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from client_info.manager import ClientInfoManager
from expert_recommendations.services import *
from expert_remarks.services import get_remark_forms, get_today_commentary


def training(request):
    """Страница для контроля тренировок"""

    if request.user.is_anonymous:
        return redirect("loginuser")

    if request.user.is_expert:
        template = "training/expertpage_training.html"

        client = User.objects.get(id=request.GET["client_id"])

        client_contacts = ClientInfoManager.get_contacts(client)
        # комментарий и заметки
        client_remark = get_remark_forms(client)

        data = {
            "clientname": client.username,
            "client_id": client.id,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
        }
        return render(request, template, data)

    if not request.user.is_expert:
        template = "training/clientpage_training.html"

        clientmemo_form = ClientInfoManager.get_clientmemo_form(request.user)

        today_commentary = get_today_commentary(request.user)

        data = {
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }
        return render(request, template, data)
