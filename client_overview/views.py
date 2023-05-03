from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from client_overview.manager import ClientInfoManager
from expert_remarks.services import get_today_commentary
from measurements.services import renew_measure_nutrition
from expert_remarks.services import get_remark_forms
from client_overview.forms import HealthQuestionaryForm, MeetQuestionaryForm
from client_overview.manager import ClientInfoManager
from client_overview.models import MeetQuestionary



@login_required
@require_http_methods(["GET"])
def overviewpage(request):
    """Страница-сводка по клиенту"""

    if request.user.is_expert:
        template = "client_overview/expert_overview_page.html"

        client = User.objects.get(id=request.GET.get("client_id"))
        client_contacts = ClientInfoManager.get_contacts(client)
        client_remark = get_remark_forms(client)

        data = {
            "client": client,
            "client_contacts": client_contacts,
            "client_remark": client_remark,
            "for_expert": True,
        }

    if not request.user.is_expert:
        template = "client_overview/client_overview_page.html"

        client = request.user
        clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
        today_commentary = get_today_commentary(client)

        data = {
            "client": client,
            "clientmemo_form": clientmemo_form,
            "today_commentary": today_commentary,
        }

    renew_measure_nutrition(client, datetime.now())

    return render(request, template, data)


@login_required
@require_http_methods(["GET", "POST"])
def meet_questionary_page(request):
    """Страница анкеты знакомства с клиентом"""

    if request.method == "GET":

        if request.user.is_expert:
            template = "client_overview/expert_meet_questionary_page.html"

            client = User.objects.get(id=request.GET.get("client_id"))
            client_contacts = ClientInfoManager.get_contacts(client)
            client_remark = get_remark_forms(client)

            data = {
                "client": client,
                "client_contacts": client_contacts,
                "client_remark": client_remark,
                "for_expert": True,
            }

        if not request.user.is_expert:
            template = "client_overview/client_meet_questionary_page.html"

            client = request.user
            clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
            today_commentary = get_today_commentary(client)

            data = {
                "client": client,
                "clientmemo_form": clientmemo_form,
                "today_commentary": today_commentary,
            }

        # TODO в template tag
        meet_questionary = ClientInfoManager.get_meet_questionary(client)
        meet_questionary_form = ClientInfoManager.get_meet_questionary_form(
            client)
        readiness_choices = MeetQuestionary.READINESS_CHOICES
        age = ClientInfoManager.get_age(client)

        data.update({
            "meet_questionary": meet_questionary,
            "meet_questionary_form": meet_questionary_form,
            "readiness_choices": readiness_choices,
            "age": age,
        })

        return render(request, template, data)
    
    # TODO переделать в ajax
    if request.method == "POST":

        form = MeetQuestionaryForm(request.POST)

        if form.is_valid():
            instance = ClientInfoManager.get_meet_questionary(request.user)

            if instance:
                form = MeetQuestionaryForm(request.POST, instance=instance)
                form.save()
                return redirect("overviewpage")
            else:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect("overviewpage")
            
        else:
            template = "client_overview/client_meet_questionary_page.html"
            client = request.user
            clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
            meet_questionary = ClientInfoManager.get_meet_questionary(client)
            meet_questionary_form = ClientInfoManager.get_meet_questionary_form(client)
            readiness_choices = MeetQuestionary.READINESS_CHOICES
            age = ClientInfoManager.get_age(request.user)
            today_commentary = get_today_commentary(request.user)

            data = {
                "client": client,
                "clientmemo_form": clientmemo_form,
                "meet_questionary": meet_questionary,
                "meet_questionary_form": meet_questionary_form,
                "readiness_choices": readiness_choices,
                "age": age,
                "today_commentary": today_commentary,
                "error": "Данные введены некорректно.",
            }
            return render(request, template, data)


@login_required
@require_http_methods(["GET", "POST"])
def health_questionary_page(request):
    """Страница анкеты здоровья клиента"""

    if request.method == "GET":

        if request.user.is_expert:
            template = "client_overview/expert_health_questionary_page.html"

            client = User.objects.get(id=request.GET.get("client_id"))
            client_contacts = ClientInfoManager.get_contacts(client)
            client_remark = get_remark_forms(client)

            data = {
                "client": client,
                "client_contacts": client_contacts,
                "client_remark": client_remark,
                "for_expert": True,
            }

        if not request.user.is_expert:
            template = "client_overview/client_health_questionary_page.html"

            client = request.user
            clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
            today_commentary = get_today_commentary(client)

            data = {
                "client": client,
                "clientmemo_form": clientmemo_form,
                "today_commentary": today_commentary,
            }

        # TODO в template tag
        health_questionary = ClientInfoManager.get_health_questionary(
            client
        )
        health_questionary_form = (
            ClientInfoManager.get_health_questionary_form(client)
        )

        data.update({
            "health_questionary": health_questionary,
            "health_questionary_form": health_questionary_form,
        })

        return render(request, template, data)
    
    # TODO переделать в ajax
    if request.method == "POST":

        form = HealthQuestionaryForm(request.POST)

        if form.is_valid():
            instance = ClientInfoManager.get_health_questionary(request.user)

            if instance:
                form = HealthQuestionaryForm(request.POST, instance=instance)
                form.save()
                return redirect("overviewpage")
            else:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect("overviewpage")
        else:
            template = "client_overview/client_health_questionary_page.html"
            client = request.user
            clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
            health_questionary = ClientInfoManager.get_health_questionary(client)
            health_questionary_form = ClientInfoManager.get_health_questionary_form(client)
            today_commentary = get_today_commentary(client)

            data = {
                "client": client,
                "clientmemo_form": clientmemo_form,
                "today_commentary": today_commentary,
                "health_questionary": health_questionary,
                "health_questionary_form": health_questionary_form,
                "error": "Данные введены некорректно. Попробуйте ещё раз.",
            }
            return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def settings_page(request):
    """Страница настроек клиента"""

    template = "client_overview/client_settings_page.html"

    client = request.user
    clientmemo_form = ClientInfoManager.get_clientmemo_form(client)
    today_commentary = get_today_commentary(client)

    data = {
        "client": client,
        "clientmemo_form": clientmemo_form,
        "today_commentary": today_commentary,
    }

    return render(request, template, data)
