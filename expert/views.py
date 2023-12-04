from datetime import date

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from chat.models import Message
from client.forms import HEALTH_FORMS, ContactsForm, HealthFormResult
from client.models import Contacts, Health, Log
from consults.forms import RequestViewForm
from consults.models import Request
from expert.decorators import expert_required
from metrics.forms import ColorsForm
from metrics.models import (
    Anthropometry,
    AnthropometryPhotoAccess as PhotoAccess,
    Colors,
    DailyData,
)
from metrics.utils import create_levels_forms
from nutrition.models import FatSecretEntry
from users.models import User


@expert_required
@require_http_methods(["GET"])
def clients(request):
    """Render the clients page for the expert"""

    clients = User.objects.filter(is_expert=False)
    new_requests = Request.objects.filter(seen=False)

    for client in clients:
        client.logs = Log.objects.filter(client=client).order_by("-id")[:10]
        client.new_messages_count = Message.objects.filter(
            sender=client, seen=False
        ).count()

    template = "expert/clients.html"
    data = {
        "clients": clients,
        "new_requests": new_requests,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def consult_requests(request):
    """Render the page for consult requests handling for the expert"""

    requests = Request.objects.all()
    new_requests = requests.filter(seen=False)
    request_forms = [RequestViewForm(instance=request) for request in requests]

    template = "expert/consult_requests.html"
    data = {
        "new_requests": new_requests,
        "request_forms": request_forms,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_registration(request):
    """Render the client registration page for the expert"""

    template = "expert/client_new.html"
    return render(request, template)


@expert_required
@require_http_methods(["GET"])
def client_profile(request, client_id):
    """
    Render the client profile page for the expert.

    Args:
        client_id (int): The ID of the client to render.
    """

    client = get_object_or_404(User, id=client_id)

    template = "expert/client_profile.html"
    data = {"client": client}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def client_health(request, client_id):
    """
    Render the client health form page for the expert.
    Saves the evaluation result.

    Args:
        client_id (int): The ID of the client to render.
    """

    client = get_object_or_404(User, id=client_id)
    health_data = Health.objects.filter(client=client).first()

    if not health_data or not health_data.is_filled:
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
    health_forms = [form(instance=health_data) for form in HEALTH_FORMS.values()]
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
    Render the client contacts page for the expert.

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
    Render metrics page of a client for the expert
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

    levels_forms = create_levels_forms(client)
    levels_colors = Colors.objects.first()

    template = "expert/client_metrics.html"
    data = {
        "client": client,
        "start_date": start or metrics[0].date,
        "end_date": end or metrics[-1].date,
        "metrics": metrics,
        "metrics_avg": metrics_avg,
        "levels_forms": levels_forms,
        "levels_colors": levels_colors,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def metrics_colors(request):
    """Handle the metrics colors form view for the expert"""

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
def client_anthropo_metrics(request, client_id):
    """Render the client's anthropometry page for the expert"""

    client = get_object_or_404(User, id=client_id)

    metrics = Anthropometry.objects.filter(client=client).order_by("id")
    photoaccess, _ = PhotoAccess.objects.get_or_create(client=client)

    template = "expert/client_anthropo_metrics.html"
    data = {
        "client": client,
        "metrics": metrics,
        "photoaccess": photoaccess,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_nutrition(request, client_id):
    """Render the client's nutrition page for the expert"""

    client = get_object_or_404(User, id=client_id)

    fs_linked = FatSecretEntry.objects.filter(client=client).exists()

    template = "expert/client_nutrition.html"
    data = {
        "client": client,
        "fatsecret_linked": fs_linked,
    }
    return render(request, template, data)
