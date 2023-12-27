from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from client.utils import create_log_entry
from config.settings import DOMAIN
from nutrition.fatsecret import FSManager
from nutrition.models import FatSecretEntry
from users.utils import get_client_id


@login_required
@require_http_methods(["GET"])
def nutrition(request):
    """Render the client's nutrition page"""

    client_id = get_client_id(request)

    fs_linked = FatSecretEntry.objects.filter(client_id=client_id).exists()
    if not fs_linked:
        return redirect(reverse("nutrition:no_fatsecret") + f"?client_id={client_id}")

    template = "nutrition/nutrition.html"
    return render(request, template)


@login_required
@require_http_methods(["GET"])
def no_fatsecret(request):
    """Render the page when no FatSecret account is linked"""

    template = "nutrition/no_fatsecret.html"
    return render(request, template)


@client_required
@require_http_methods(["GET"])
def link_fatsecret(request):
    """
    This function is used to link the user's FatSecret account with our application.

    It performs the following steps:
    1. If the oauth_verifier is not provided in the request parameters,
       it redirects the user to the FatSecret authorization URL (and gets verifier).
    2. If the oauth_verifier is provided, it authenticates the user
       with FatSecret using the oauth_verifier and saves the tokens for future access.
    """

    client = request.user
    oauth_verifier = request.GET.get("oauth_verifier")
    callback_url = "http://" + DOMAIN + reverse("nutrition:link_fatsecret")

    fs = FSManager()

    # Step 1: Redirect the user to the FatSecret authorization URL
    if oauth_verifier is None:
        auth_url = fs.session.get_authorize_url(callback_url)
        fs.save_session(client.id)
        return redirect(auth_url)

    # Step 2: Authenticate the user with FatSecret and save the tokens
    # (session must be the same!)
    try:
        fs.load_session(client.id)
        tokens = fs.session.authenticate(oauth_verifier)
        fs.save_tokens(client_tokens=tokens, client=client)
        create_log_entry(
            modelname="Данные FatSecret",
            description="Аккаунт успешно подключен!",
            client=client,
            link=reverse("nutrition:nutrition") + f"?client_id={client.id}",
        )
        return redirect("nutrition:nutrition")

    except KeyError as error:
        print("Link fatsecret error:", error)
        auth_url = fs.session.get_authorize_url(callback_url)
        return redirect(auth_url)
