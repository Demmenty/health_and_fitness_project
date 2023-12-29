from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from authentication.forms import ClientRegistrationForm


@require_http_methods(["POST"])
def client_registration(request):
    """Обработка запроса регистрации нового клиента"""

    form = ClientRegistrationForm(request.POST)

    if form.is_valid():
        user = User.objects.create_user(
            request.POST["username"], password=request.POST["password1"]
        )
        user.save()
        return HttpResponse()
    else:
        return JsonResponse(form.errors, status=400)


@require_http_methods(["POST"])
def loginuser(request):
    """Обработка запроса входа пользователя"""

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
