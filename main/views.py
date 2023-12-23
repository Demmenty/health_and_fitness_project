from django.shortcuts import render

from consults.forms import NewRequestForm
from users.forms import UserLoginForm


def home(request):
    """View for website home page"""

    template = "main/home.html"
    data = {
        "login_form": UserLoginForm(),
        "consult_request_form": NewRequestForm(),
    }
    return render(request, template, data)
