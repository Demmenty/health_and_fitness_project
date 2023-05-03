from datetime import datetime
from expert_remarks.services import get_today_commentary
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from measurements.utils import *
from django.views.decorators.http import require_http_methods
from client_overview.manager import ClientInfoManager
from expert_recommendations.services import *
from expert_remarks.services import get_remark_forms
from fatsecret_app.services import *
from measurements.services import *



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
@require_http_methods(["GET", "POST"])
def addmeasurepage(request):
    """Страница редактирования физических измерений клентом"""

    client = request.user

    if request.method == "GET":
        template = "measurements/client_addmeasure_page.html"

        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        weekly_measure_forms = create_weekly_measure_forms(client)
        fatsecret_connected = services.fs.is_connected(client)
        if fatsecret_connected:
            renew_weekly_measures_nutrition(client)

        last_seven_dates = _create_list_of_dates(7)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "fatsecret_connected": fatsecret_connected,
            "weekly_measure_forms": weekly_measure_forms,
            "last_seven_dates": last_seven_dates,
            "today_commentary": today_commentary,
        }
        return render(request, template, data)
    
    # TODO переделать в ajax
    if request.method == "POST":
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)

        fatsecret_connected = services.fs.is_connected(client)
        form = MeasurementForm(request.POST)

        if form.is_valid():
            measure_date = form.cleaned_data["date"]
            measure_weight = form.cleaned_data["weight"]

            if fatsecret_connected and measure_weight:
                services.fs.send_weight(
                    client, measure_weight, measure_date
                )

            instance = get_daily_measure(client, measure_date)
            if instance:
                form = MeasurementForm(request.POST, instance=instance)
                form.save()
                return redirect("measurementspage")
            else:
                addmeasure_error = (
                    "Случилось что-то непонятное, либо вы читерите :("
                )
        else:
            addmeasure_error = (
                "Данные введены некорректно. Попробуйте еще раз."
            )

        weekly_measure_forms = create_weekly_measure_forms(request.user)
        last_seven_dates = _create_list_of_dates(7)
        today_commentary = get_today_commentary(request.user)
        template = "measurements/client_addmeasure_page.html"

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "addmeasure_error": addmeasure_error,
            "fatsecret_connected": fatsecret_connected,
            "weekly_measure_forms": weekly_measure_forms,
            "last_seven_dates": last_seven_dates,
            "today_commentary": today_commentary,
        }
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
