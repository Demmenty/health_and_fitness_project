from datetime import date

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from client.forms import HEALTH_FORMS, ContactsForm, HealthFormResult
from client.models import Contacts, Health, MainData
from expert.decorators import expert_required
from home.models import ConsultRequest
from metrics.forms import ColorsForm, NutritionRecsForm
from metrics.models import Colors, DailyData, NutritionRecs
from metrics.utils import create_levels_forms
from nutrition.models import FatSecretEntry
from users.models import User


@expert_required
@require_http_methods(["GET"])
def clients(request):
    """
    Render the clients page for the expert account.
    """
    clients = User.objects.filter(is_expert=False)
    unread_requests = ConsultRequest.objects.filter(is_read=False)
    unread_requests_amount = unread_requests.count()

    template = "expert/clients.html"
    data = {
        "clients": clients,
        "unread_requests_amount": unread_requests_amount,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_registration(request):
    """
    Render the client registration page for the expert account.
    """
    template = "expert/client_new.html"
    return render(request, template)


@expert_required
@require_http_methods(["GET"])
def client_profile(request, client_id):
    """
    Render the client profile page for the expert account.

    Args:
        client_id (int): The ID of the client to render.
    """
    client = get_object_or_404(User, id=client_id)
    maindata = MainData.objects.filter(client=client).first()

    template = "expert/client_profile.html"
    data = {
        "client": client,
        "maindata": maindata,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def client_health(request, client_id):
    """
    Render the client health form page for the expert account.
    Saves the evaluation result.

    Args:
        client_id (int): The ID of the client to render.
    """
    client = get_object_or_404(User, id=client_id)
    health_data = Health.objects.filter(client=client).first()

    if not health_data:
        template = "expert/client_health.html"
        data = {"client": client}
        return render(request, template, data)

    if request.method == "GET":
        result_form = HealthFormResult(instance=health_data)

    if request.method == "POST":
        result_form = HealthFormResult(request.POST, instance=health_data)
        if result_form.is_valid():
            result_form.save()
            return redirect("expert:client_profile", client_id)

    template = "expert/client_health.html"
    health_forms = [
        form(instance=health_data) for form in HEALTH_FORMS.values()
    ]
    data = {
        "client": client,
        "health_data": health_data,
        "health_forms": health_forms,
        "result_form": result_form,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_contacts(request, client_id):
    """
    Render the client contacts page.

    Args:
        client_id (int): The ID of the client.
    """
    client = get_object_or_404(User, id=client_id)
    contacts = Contacts.objects.filter(client=client).first()
    contacts_form = ContactsForm(instance=contacts)

    template = "expert/client_contacts.html"
    data = {
        "client": client,
        "contacts_form": contacts_form,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_metrics(request, client_id):
    """
    A view function that shows the metrics of a client
    within a specified date range or number of days.
    """
    client = get_object_or_404(User, id=client_id)
    start = request.GET.get("start")
    end = request.GET.get("end")
    days = int(request.GET.get("days", 7))

    if start and end:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        metrics = DailyData.objects.get_by_date_range(client, start, end)
    else:
        metrics = DailyData.objects.get_by_days(client, days)

    metrics = DailyData.update_nutrition_from_fs(metrics)
    metrics_avg = DailyData.get_avg(metrics, count_today_nutrition=False)

    recommendatons = NutritionRecs.objects.filter(client=client).first()
    recommedations_form = NutritionRecsForm(instance=recommendatons)

    levels_forms = create_levels_forms(client)
    levels_colors = Colors.objects.first()

    template = "expert/client_metrics.html"
    data = {
        "client": client,
        "start_date": start or metrics[0].date,
        "end_date": end or metrics[-1].date,
        "metrics": metrics,
        "metrics_avg": metrics_avg,
        "recommedations_form": recommedations_form,
        "levels_forms": levels_forms,
        "levels_colors": levels_colors,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def metrics_colors(request):
    """
    Handle the metrics colors form view.
    """
    instance = Colors.objects.first()
    form = ColorsForm(instance=instance)

    if request.method == "POST":
        form = ColorsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            next = request.GET.get("next")
            if next:
                return redirect(next)

    template = "expert/metrics_colors.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_nutrition(request, client_id):
    """
    A view function that shows the client's nutrition page.
    """
    client = get_object_or_404(User, id=client_id)

    fatsecret_is_linked = FatSecretEntry.objects.filter(client=client).exists()
    recommendatons = NutritionRecs.objects.filter(client=client).first()
    recommedations_form = NutritionRecsForm(instance=recommendatons)

    template = "expert/client_nutrition.html"
    data = {
        "client": client,
        "fatsecret_is_linked": fatsecret_is_linked,
        "recommedations_form": recommedations_form,
    }
    return render(request, template, data)
