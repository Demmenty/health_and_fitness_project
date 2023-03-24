from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render

from consultation_signup.forms import ConsultationsignupForm


def homepage(request):
    """Главная страница сайта"""

    data = {
        "registration_form": UserCreationForm(),
        "login_form": AuthenticationForm,
        "consultation_form": ConsultationsignupForm(),
    }

    return render(request, "homepage/homepage.html", data)
