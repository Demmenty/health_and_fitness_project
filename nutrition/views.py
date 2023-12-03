from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from config.settings import DOMAIN_NAME
from nutrition.fatsecret import FSManager


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

    oauth_verifier = request.GET.get("oauth_verifier")
    callback_url = DOMAIN_NAME + reverse("nutrition:link_fatsecret")

    fs = FSManager()

    # Step 1: Redirect the user to the FatSecret authorization URL
    if oauth_verifier is None:
        auth_url = fs.session.get_authorize_url(callback_url)
        fs.save_session(request.user.id)
        return redirect(auth_url)

    # Step 2: Authenticate the user with FatSecret and save the tokens
    # (session must be the same!)
    try:
        fs.load_session(request.user.id)
        tokens = fs.session.authenticate(oauth_verifier)
        fs.save_tokens(client_tokens=tokens, client=request.user)
        return redirect("client:nutrition")

    except KeyError as error:
        print("Link fatsecret error:", error)
        auth_url = fs.session.get_authorize_url(callback_url)
        return redirect(auth_url)
