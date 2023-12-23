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
    ProfileForm,
    UserEmailForm,
)
from client.models import Contacts, Health
from nutrition.models import FatSecretEntry


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
