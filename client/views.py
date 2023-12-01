from datetime import date

from django.forms import ModelForm
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from client.forms import (
    FIRST_HEALTH_FORM_PAGE,
    HEALTH_FORMS,
    LAST_HEALTH_FORM_PAGE,
    ContactsForm,
    UserEmailForm,
    UserInfoForm,
)
from client.models import Contacts, Health
from metrics.forms import DailyDataForm
from metrics.models import DailyData
from nutrition.models import FatSecretEntry


@client_required
@require_http_methods(["GET"])
def profile(request):
    """Render the profile page for a client"""

    template = "client/profile.html"
    return render(request, template)


@client_required
@require_http_methods(["GET", "POST"])
def health(request, page: int):
    """
    Handle the health form submission and rendering for a client.

    Args:
        page (int): The current page number of the health form section.
    """

    form_class = HEALTH_FORMS.get(page)
    if not form_class:
        raise Http404

    if page == LAST_HEALTH_FORM_PAGE:
        next_page_url = reverse_lazy("client:profile")
    else:
        next_page_url = reverse_lazy("client:health", kwargs={"page": page + 1})

    instance = Health.objects.filter(client=request.user).first()

    if page == FIRST_HEALTH_FORM_PAGE and instance:
        return redirect(next_page_url)
    elif page != FIRST_HEALTH_FORM_PAGE and not instance:
        return redirect("client:profile")

    if request.method == "GET":
        form: ModelForm = form_class(instance=instance)

    if request.method == "POST":
        form: ModelForm = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect(next_page_url)

    template = "client/health_form.html"
    data = {
        "form": form,
        "page": page,
        "last_page": LAST_HEALTH_FORM_PAGE,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def info(request):
    """Handle the client's main information"""

    if request.method == "GET":
        form = UserInfoForm(instance=request.user)

    if request.method == "POST":
        form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:profile")

    template = "client/info.html"
    data = {"form": form}
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def contacts(request):
    """Handle the client's contacts forms"""

    contacts = Contacts.objects.filter(client=request.user).first()

    if request.method == "GET":
        email_form = UserEmailForm(instance=request.user)
        contacts_form = ContactsForm(instance=contacts)

    if request.method == "POST":
        email_form = UserEmailForm(request.POST, instance=request.user)
        contacts_form = ContactsForm(request.POST, instance=contacts)

        if email_form.is_valid() and contacts_form.is_valid():
            contacts_form.instance.client = request.user
            contacts_form.save()
            email_form.save()
            return redirect("client:profile")

    template = "client/contacts.html"
    help_img_folder = "/static/client/img/contacts-help/"
    data = {
        "contacts_form": contacts_form,
        "email_form": email_form,
        "help_img_folder": help_img_folder,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET"])
def metrics(request):
    """
    Render the metrics page for a client
    within a specified date range or number of days.
    """

    client = request.user

    start = request.GET.get("start")
    end = request.GET.get("end")

    if start and end:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        metrics = DailyData.objects.get_by_date_range(client, start, end)
    else:
        days = int(request.GET.get("days", 7))
        metrics = DailyData.objects.get_by_days(client, days)

    metrics = DailyData.update_nutrition_from_fs(metrics)
    metrics_avg = DailyData.get_avg(metrics, count_today_nutrition=False)

    template = "client/metrics.html"
    data = {
        "start_date": start or metrics[0].date,
        "end_date": end or metrics[-1].date,
        "metrics": metrics,
        "metrics_avg": metrics_avg,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def metrics_add(request):
    """Handle the client's metrics form"""

    client = request.user

    if request.method == "GET":
        metrics_date = request.GET.get("date", date.today())
        form = DailyDataForm.get_form(client, metrics_date)

    if request.method == "POST":
        form = DailyDataForm(request.POST)
        if form.is_valid():
            instance = DailyData.objects.filter(
                date=form.cleaned_data["date"], client=client
            ).first()
            form = DailyDataForm(request.POST, instance=instance)
            form.instance.client = client
            form.save()
            return redirect("client:metrics")

    template = "client/metrics_add.html"
    data = {
        "daily_metrics_form": form,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET"])
def nutrition(request):
    """Render the client's nutrition page"""

    client = request.user

    fatsecret_linked = FatSecretEntry.objects.filter(client=client).exists()
    if not fatsecret_linked:
        return redirect("client:link_fatsecret")

    template = "client/nutrition.html"
    return render(request, template)


@client_required
@require_http_methods(["GET"])
def link_fatsecret(request):
    """Render the page offering to link Fatsecret."""

    template = "client/link_fatsecret.html"
    return render(request, template)
