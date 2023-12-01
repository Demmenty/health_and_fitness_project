from django.shortcuts import render

from consults.forms import NewRequestForm
from users.forms import UserLoginForm


def main(request):
    """View for website main page"""

    template = "home/main.html"

    data = {
        "login_form": UserLoginForm(),
        "consult_request_form": NewRequestForm(),
    }
    return render(request, template, data)
