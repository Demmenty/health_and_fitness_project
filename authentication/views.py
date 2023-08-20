from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import redirect


def registration(request):
    """Обработка запроса регистрации пользователя"""

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                request.POST["username"], password=request.POST["password1"]
            )
            user.save()
            login(request, user)
            return HttpResponse()

        else:
            return JsonResponse(form.errors, status=400)


def loginuser(request):
    """Обработка запроса входа пользователя"""

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return HttpResponseForbidden("Пароль или логин введены неверно")

        login(request, user)

        data = {
            "is_expert": user.is_expert,
        }
        return JsonResponse(data, status=200)


@login_required
def logoutuser(request):
    """Обработка запроса выхода пользователя"""

    if request.method == "POST":
        logout(request)

    return redirect("homepage")
