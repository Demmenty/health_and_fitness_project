from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from client_overview.manager import ClientInfoManager
from expert_recommendations.services import *
from expert_remarks.services import get_remark_forms, get_today_commentary
from fatsecret_app.services import *
from measurements.services import *
from measurements.utils import *


@login_required
@require_http_methods(["GET"])
def measurementspage(request):
    """Страница отслеживания физических измерений"""

    if request.user.is_expert:
        template = "measurements/expert_measurements_page.html"

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
        template = "measurements/client_measurements_page.html"

        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    renew_measure_nutrition(client, datetime.now())
    renew_weekly_measures_nutrition(client)

    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def anthropometrypage(request):
    """Страница антропометрических измерений"""

    if request.user.is_expert:
        template = "measurements/expert_anthropometry_page.html"

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
        template = "measurements/client_anthropometry_page.html"

        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    return render(request, template, data)


def _create_list_of_dates(days: int) -> list:
    list_of_dates = []

    for i in range(days):
        selected_date = date.today() - timedelta(days=(6 - i))
        list_of_dates.append(selected_date)

    return list_of_dates
