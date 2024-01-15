from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from expert.decorators import expert_required
from metrics.forms import AnthropoMetricsForm, ColorsForm, DailyMetricsForm
from metrics.models import (
    Anthropo as AnthropoMetrics,
    Colors,
    Daily as DailyMetrics,
    PhotoAccess,
)
from metrics.utils import create_levels_forms
from users.utils import get_client


@login_required
@require_http_methods(["GET"])
def daily(request):
    """
    Render client's daily metrics page
    within a specified date range or number of days.
    """

    client = get_client(request)
    start = request.GET.get("start")
    end = request.GET.get("end")
    days = int(request.GET.get("days", 7))
    show_chart = request.GET.get("show_chart", False)
    chart_param = request.GET.get("chart_param", "")

    if start and end:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        metrics = DailyMetrics.objects.get_by_date_range(client, start, end)
    else:
        metrics = DailyMetrics.objects.get_by_days(client, days)

    metrics = DailyMetrics.update_nutrition_from_fs(metrics)
    metrics_avg = DailyMetrics.get_avg(metrics, count_today_nutrition=False)

    template = "metrics/daily.html"
    data = {
        "start_date": start or metrics[0].date,
        "end_date": end or metrics[-1].date,
        "metrics": metrics,
        "metrics_avg": metrics_avg,
        "show_chart": show_chart,
        "chart_param": chart_param,
    }

    if request.user.is_expert:
        levels_forms = create_levels_forms(client)
        levels_colors = Colors.objects.first()
        data.update(
            {
                "levels_forms": levels_forms,
                "levels_colors": levels_colors,
            }
        )

    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def daily_edit(request):
    """Handle the client's daily metrics form"""

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
            return redirect("metrics:daily")

    template = "metrics/daily_form.html"
    data = {"form": form}
    return render(request, template, data)


@expert_required
@require_http_methods(["GET", "POST"])
def colors(request):
    """Render the metrics colors form"""

    instance = Colors.objects.first()
    form = ColorsForm(instance=instance)

    if request.method == "POST":
        form = ColorsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            next = request.GET.get("next")
            if next:
                return redirect(next)

    template = "metrics/colors.html"
    data = {"form": form}
    return render(request, template, data)


@login_required
@require_http_methods(["GET"])
def anthropo(request):
    """Render the client's anthropometry page"""

    client = get_client(request)

    metrics = AnthropoMetrics.objects.filter(client=client).order_by("id")
    photoaccess, _ = PhotoAccess.objects.get_or_create(client=client)

    template = "metrics/anthropo.html"
    data = {
        "metrics": metrics,
        "photoaccess": photoaccess,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def anthropo_add(request):
    """View function for creating a new anthropometry entry"""

    if request.method == "GET":
        form = AnthropoMetricsForm()

    if request.method == "POST":
        form = AnthropoMetricsForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("metrics:anthropo")

    template = "metrics/anthropo_form.html"
    data = {"form": form}
    return render(request, template, data)
