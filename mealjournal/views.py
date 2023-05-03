from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from client_overview.manager import ClientInfoManager
from expert_remarks.services import get_remark_forms, get_today_commentary
from expert_recommendations.services import *


@login_required
@require_http_methods(["GET"])
def mealjournal_page(request):
    """Страница контроля за питанием"""

    if request.user.is_expert:
        template = "mealjournal/expert_mealjournal_page.html"

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
        template = "mealjournal/client_mealjournal_page.html"
        
        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def foodbydate_page(request):
    """Страница питания за день"""

    if request.user.is_expert:
        template = "mealjournal/expert_foodbydate_page.html"

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
        template = "mealjournal/client_foodbydate_page.html"
        
        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def foodbymonth_page(request):
    """Страница питания за месяц"""

    if request.user.is_expert:
        template = "mealjournal/expert_foodbymonth_page.html"

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
        template = "mealjournal/client_foodbymonth_page.html"
        
        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    return render(request, template, data)
