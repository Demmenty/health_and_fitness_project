from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from expert.decorators import expert_required
from subscriptions.forms import PlanForm, SubscriptionForm
from subscriptions.models import Plan, Subscription
from users.models import User


@client_required
@require_http_methods(["GET"])
def subscription_detail(request):
    """Renders the details of a subscription of the current user."""

    subscription = get_object_or_404(Subscription, client=request.user)

    template = "subscriptions/subscription_detail.html"
    data = {"subscription": subscription}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def edit_subscription(request, client_id):
    """Renders the form for editing, creating or deleting a subscription by user id."""

    client = get_object_or_404(User, id=client_id)
    subscription = client.subscription if hasattr(client, "subscription") else None

    if request.method == "GET":
        initial_data = (
            {"start_date": timezone.now().strftime("%Y-%m-%d")}
            if not subscription
            else None
        )
        form = SubscriptionForm(initial=initial_data, instance=subscription)

    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)

        if subscription and not form.data.get("plan"):
            client.subscription.delete()
        elif form.is_valid():
            form.instance.client = client
            form.save()

        return redirect(reverse("expert:client_profile") + f"?client_id={client_id}")

    template = "subscriptions/subscription_form.html"
    data = {
        "form": form,
        "client": client,
    }
    return render(request, template, data)


@expert_required
@require_http_methods(["GET"])
def plans(request):
    """Renders the list of available subscription plans."""

    plans = Plan.objects.all()

    template = "subscriptions/plans.html"
    data = {"plans": plans}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def new_plan(request):
    """Renders the form for creating a new subscription plan."""

    if request.method == "GET":
        form = PlanForm()

    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subscription:plans")

    template = "subscriptions/plan_form.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def edit_plan(request, plan_id):
    """Renders the form for editing a subscription plan."""

    plan = get_object_or_404(Plan, id=plan_id)

    if request.method == "GET":
        form = PlanForm(instance=plan)

    if request.method == "POST":
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("subscription:plans")

    template = "subscriptions/plan_form.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["POST"])
def delete_plan(request, plan_id):
    """Deletes a subscription plan."""

    plan = get_object_or_404(Plan, id=plan_id)
    plan.delete()

    return redirect("subscription:plans")
