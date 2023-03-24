from django.shortcuts import render, redirect
from expert_remarks.services import get_today_commentary
from client_info.services import get_clientmemo_form_for
from fatsecret_app.services import *
from measurements.services import *
from expert_recommendations.services import *
from anthropometry.services import *
from client_info.services import *
from expert_remarks.services import get_remark_forms
from django.contrib.auth.models import User


def training(request):
    """Страница для контроля тренировок"""

    if request.user.is_anonymous:
        return redirect("loginuser")
    
    if request.user.is_expert:
        template = "training/expertpage_training.html"
        # определение клиента
        client_id = request.GET["client_id"]
        client = User.objects.get(id=client_id)

        # контакты клиента
        client_contacts = get_contacts_of(client)
        # комментарий и заметки
        client_remark = get_remark_forms(client)

        data = {
            "clientname": client.username,
            "client_id": client_id,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
        }
        return render(request, template, data)

    if not request.user.is_expert:
        template = "training/clientpage_training.html"

        clientmemo_form = get_clientmemo_form_for(request.user)

        # комментарий за сегодня от эксперта
        today_commentary = get_today_commentary(request.user)

        data = {
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }
        return render(request, template, data)
