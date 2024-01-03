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
    FeedbackForm,
    FoodForm,
    GoalForm,
    ProfileForm,
    SleepForm,
    UserEmailForm,
    WeightForm,
)
from client.models import Contacts, Feedback, Food, Goal, Health, Sleep, Weight


@client_required
@require_http_methods(["GET"])
def profile(request):
    """Render the client's profile page"""

    template = "client/profile.html"
    return render(request, template)


@client_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    """Handle the client's profile form"""

    if request.method == "GET":
        form = ProfileForm(instance=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:profile")

    template = "client/profile_form.html"
    data = {"form": form}
    return render(request, template, data)


@client_required
@require_http_methods(["GET"])
def questionnaires(request):
    """Render the client's questionnaires selection page"""

    template = "client/questionnaires.html"
    return render(request, template)


@client_required
@require_http_methods(["GET", "POST"])
def weight(request):
    """Handle the client's weight form submission and rendering"""

    instance = Weight.objects.filter(client=request.user).first()

    if request.method == "GET":
        form = WeightForm(instance=instance)

    if request.method == "POST":
        form = WeightForm(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:questionnaires")

    template = "client/weight.html"
    data = {"form": form}
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def sleep(request):
    """Handle the client's sleep form submission and rendering"""

    instance = Sleep.objects.filter(client=request.user).first()

    if request.method == "GET":
        form = SleepForm(instance=instance)

    if request.method == "POST":
        form = SleepForm(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:questionnaires")

    template = "client/sleep.html"
    data = {"form": form}
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def food(request):
    """Handle the client's food form submission and rendering"""

    instance = Food.objects.filter(client=request.user).first()

    if request.method == "GET":
        form = FoodForm(instance=instance)

    if request.method == "POST":
        form = FoodForm(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:questionnaires")

    template = "client/food.html"
    data = {"form": form}
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def goal(request):
    """Handle the client's goal form submission and rendering"""

    instance = Goal.objects.filter(client=request.user).first()

    if request.method == "GET":
        form = GoalForm(instance=instance)

    if request.method == "POST":
        form = GoalForm(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:questionnaires")

    template = "client/goal.html"
    data = {"form": form}
    return render(request, template, data)


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
        next_page_url = reverse_lazy("client:questionnaires")
    else:
        next_page_url = reverse_lazy("client:health", kwargs={"page": page + 1})

    instance = Health.objects.filter(client=request.user).first()

    if page == FIRST_HEALTH_FORM_PAGE and instance:
        return redirect(next_page_url)
    elif page != FIRST_HEALTH_FORM_PAGE and not instance:
        return redirect("client:questionnaires")

    if request.method == "GET":
        form = form_class(instance=instance)

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
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
def contacts(request):
    """Handle the client's contacts forms"""

    instance = Contacts.objects.filter(client=request.user).first()

    if request.method == "GET":
        email_form = UserEmailForm(instance=request.user)
        form = ContactsForm(instance=instance)

    if request.method == "POST":
        email_form = UserEmailForm(request.POST, instance=request.user)
        form = ContactsForm(request.POST, instance=instance)

        if email_form.is_valid() and form.is_valid():
            form.instance.client = request.user
            form.save()
            email_form.save()
            return redirect("client:profile")

    template = "client/contacts.html"
    help_img_folder = "/static/client/img/contacts-help/"
    data = {
        "form": form,
        "email_form": email_form,
        "help_img_folder": help_img_folder,
    }
    return render(request, template, data)


@client_required
@require_http_methods(["GET", "POST"])
def feedback(request):
    """Handle the client's feedback form"""

    instance = Feedback.objects.filter(client=request.user).first()

    if request.method == "GET":
        form = FeedbackForm(instance=instance)

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=instance)
        if form.is_valid():
            form.instance.client = request.user
            form.save()
            return redirect("client:profile")

    template = "client/feedback.html"
    data = {"form": form}
    return render(request, template, data)
