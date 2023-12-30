from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from chat.models import Message
from client.forms import (
    HEALTH_FORMS,
    ContactsForm,
    FoodForm,
    GoalForm,
    HealthFormResult,
    SleepForm,
    WeightForm,
)
from client.models import Contacts, Food, Goal, Health, Log, Sleep, Weight
from consults.forms import RequestViewForm
from consults.models import Request
from expert.decorators import expert_required
from users.models import User
from users.utils import get_client_id


@expert_required
@require_http_methods(["GET"])
def clients(request):
    """Render the clients page for the expert"""

    clients = User.objects.filter(is_expert=False, is_active=True)

    for client in clients:
        client.logs = Log.objects.filter(client=client).order_by("-id")[:10]
        client.new_messages_count = Message.objects.filter(
            sender=client, seen=False
        ).count()

    template = "expert/clients.html"
    data = {"clients": clients}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def archived_clients(request):
    """Render the archived clients page for the expert"""

    clients = User.objects.filter(is_expert=False, is_active=False)

    template = "expert/clients.html"
    data = {"clients": clients}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_new(request):
    """Render the client registration page for the expert"""

    template = "expert/client_new.html"
    return render(request, template)


@expert_required
@require_http_methods(["GET"])
def client_profile(request):
    """Render the client profile page for the expert."""

    template = "expert/client_profile.html"
    return render(request, template)


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
@require_http_methods(["POST"])
def client_delete(request, id):
    """Delete a client's account"""

    client = get_object_or_404(User, id=id)
    client.delete()

    return redirect("expert:archived_clients")


@expert_required
@require_http_methods(["GET"])
def client_questionnaires(request):
    """Render the client's questionnaires selection page"""

    template = "client/questionnaires.html"
    return render(request, template)


@expert_required
@require_http_methods(["GET"])
def client_weight(request):
    """Render the client's weight form"""

    client_id = get_client_id(request)
    instance = Weight.objects.filter(client_id=client_id).first()
    form = WeightForm(instance=instance)
    for field in form.fields.values():
        field.widget.attrs["disabled"] = True

    template = "client/weight.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_sleep(request):
    """Render the client's sleep form"""

    client_id = get_client_id(request)
    instance = Sleep.objects.filter(client_id=client_id).first()
    form = SleepForm(instance=instance)
    for field in form.fields.values():
        field.widget.attrs["disabled"] = True

    template = "client/sleep.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_food(request):
    """Render the client's food form"""

    client_id = get_client_id(request)
    instance = Food.objects.filter(client_id=client_id).first()
    form = FoodForm(instance=instance)
    for field in form.fields.values():
        field.widget.attrs["disabled"] = True

    template = "client/food.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_goal(request):
    """Render the client's goal form"""

    client_id = get_client_id(request)
    instance = Goal.objects.filter(client_id=client_id).first()
    form = GoalForm(instance=instance)
    for field in form.fields.values():
        field.widget.attrs["disabled"] = True

    template = "client/goal.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def client_health(request):
    """
    GET: Render the client health form page for the expert.
    POST: Saves the health evaluation result.
    """

    client_id = get_client_id(request)
    instance = Health.objects.filter(client_id=client_id).first()

    if request.method == "GET":
        result_form = HealthFormResult(instance=instance)

    if request.method == "POST":
        result_form = HealthFormResult(request.POST, instance=instance)
        if result_form.is_valid():
            result_form.save()
            return redirect(
                reverse("expert:client_questionnaires") + f"?client_id={client_id}"
            )

    forms = [form(instance=instance) for form in HEALTH_FORMS.values()]
    for form in forms:
        for field in form.fields.values():
            field.widget.attrs["disabled"] = True

    template = "expert/client_health.html"
    data = {
        "instance": instance,
        "forms": forms,
        "result_form": result_form,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def client_contacts(request):
    """Render the client contacts page for the expert"""

    client_id = get_client_id(request)
    instance = Contacts.objects.filter(client_id=client_id).first()
    form = ContactsForm(instance=instance)
    for field in form.fields.values():
        field.widget.attrs["disabled"] = True

    template = "expert/client_contacts.html"
    data = {"form": form}
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
