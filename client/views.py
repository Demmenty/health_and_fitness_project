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
from metrics.forms import AnthropoMetricsForm, DailyMetricsForm
from metrics.models import (
    Anthropo as AnthropoMetrics,
    Daily as DailyMetrics,
    PhotoAccess,
)
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

    template = "client/health.html"
    data = {
        "form": form,
        "page": page,
        "last_page": LAST_HEALTH_FORM_PAGE,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def info(request):
    """Handle the client's main information form"""

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
def daily_metrics(request):
    """
    Render the daily metrics page for a client
    within a specified date range or number of days.
    """

    client = request.user

    start = request.GET.get("start")
    end = request.GET.get("end")

    if start and end:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        metrics = DailyMetrics.objects.get_by_date_range(client, start, end)
    else:
        days = int(request.GET.get("days", 7))
        metrics = DailyMetrics.objects.get_by_days(client, days)

    metrics = DailyMetrics.update_nutrition_from_fs(metrics)
    metrics_avg = DailyMetrics.get_avg(metrics, count_today_nutrition=False)

    template = "client/daily_metrics.html"
    data = {
        "start_date": start or metrics[0].date,
        "end_date": end or metrics[-1].date,
        "metrics": metrics,
        "metrics_avg": metrics_avg,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def daily_metrics_edit(request):
    """
    Handle the client's daily metrics form.
    GET: Displays the form with existing metrics data.
    POST: Saves or updates the metrics data.
    """

    client = request.user

    if request.method == "GET":
        metrics_date = request.GET.get("date", date.today())
        form = DailyMetricsForm.get_form(client, metrics_date)

    if request.method == "POST":
        form = DailyMetricsForm(request.POST)
        if form.is_valid():
            metrics_date = form.cleaned_data["date"]
            instance = DailyMetrics.objects.filter(
                date=metrics_date, client=client
            ).first()
            form = DailyMetricsForm(request.POST, instance=instance)
            form.instance.client = client
            form.save()
            return redirect("client:daily_metrics")

    template = "client/daily_metrics_form.html"
    data = {
        "daily_metrics_form": form,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET"])
def anthropo_metrics(request):
    """Render the client's anthropometry page"""

    client = request.user

    metrics = AnthropoMetrics.objects.filter(client=client).order_by("id")
    photoaccess, _ = PhotoAccess.objects.get_or_create(client=client)

    template = "client/anthropo_metrics.html"
    data = {
        "metrics": metrics,
        "photoaccess": photoaccess,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def anthropo_metrics_new(request):
    """View function for creating a new anthropometry entry"""

    client = request.user

    if request.method == "GET":
        form = AnthropoMetricsForm()

    if request.method == "POST":
        form = AnthropoMetricsForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.client = client
            form.save()
            return redirect("client:anthropo_metrics")

    template = "client/anthropo_metrics_form.html"
    data = {"form": form}
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
