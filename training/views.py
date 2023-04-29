from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from client_info.manager import ClientInfoManager
from expert_remarks.services import get_remark_forms, get_today_commentary


# TODO сделать классом и переименовать в TrainingView
def training(request):
    """Страница для контроля тренировок"""

    if request.user.is_anonymous:
        return redirect("loginuser")

    if request.user.is_expert:
        template = "training/expertpage.html"

        client = User.objects.get(id=request.GET["client_id"])
        client_contacts = ClientInfoManager.get_contacts(client)
        client_remark = get_remark_forms(client)

        data = {
            "client": client,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
            "for_expert": True,
        }
        return render(request, template, data)

    if not request.user.is_expert:
        template = "training/clientpage.html"
        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }
        return render(request, template, data)
