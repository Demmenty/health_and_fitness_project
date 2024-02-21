from django.shortcuts import render

from consults.forms import NewRequestForm
from users.forms import UserLoginForm


def home(request):
    """Renders the home page"""

    template = "main/home.html"
    data = {
        "login_form": UserLoginForm(),
        "consult_request_form": NewRequestForm(),
    }
    return render(request, template, data)


def maintenance(request):
    """Renders the maintenance page"""

    template = "main/maintenance.html"
    return render(request, template)
