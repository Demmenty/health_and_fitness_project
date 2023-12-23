from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from chat.models import Message
from client.forms import HEALTH_FORMS, ContactsForm, HealthFormResult
from client.models import Contacts, Health, Log
from consults.forms import RequestViewForm
from consults.models import Request
from expert.decorators import expert_required
from users.models import User


@expert_required
@require_http_methods(["GET"])
def clients(request):
    """Render the clients page for the expert"""

    clients = User.objects.filter(is_expert=False, is_active=True)
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
def archived_clients(request):
    """Render the archived clients page for the expert"""

    clients = User.objects.filter(is_expert=False, is_active=False)
    new_requests = Request.objects.filter(seen=False)

    template = "expert/clients.html"
    data = {
        "clients": clients,
        "new_requests": new_requests,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_new(request):
    """Render the client registration page for the expert"""

    template = "expert/client_new.html"
    return render(request, template)


@expert_required
@require_http_methods(["GET"])
def client_profile(request, id):
    """Render the client profile page for the expert."""

    client = get_object_or_404(User, id=id)

    template = "expert/client_profile.html"
    data = {"client": client}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_archive(request, id):
    """Archive a client's account by making it inactive"""

    client = get_object_or_404(User, id=id)
    client.is_active = False
    client.save()

    return redirect("expert:clients")


@expert_required
@require_http_methods(["GET"])
def client_unarchive(request, id):
    """Unarchive a client's account by making it active"""

    client = get_object_or_404(User, id=id)
    client.is_active = True
    client.save()

    return redirect("expert:archived_clients")


@expert_required
@require_http_methods(["GET", "POST"])
def client_health(request, id):
    """
    GET: Render the client health form page for the expert.
    POST: Saves the health evaluation result.
    """

    client = get_object_or_404(User, id=id)
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
            return redirect("expert:client_profile", id)

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
def client_contacts(request, id):
    """Render the client contacts page for the expert"""

    client = get_object_or_404(User, id=id)
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
