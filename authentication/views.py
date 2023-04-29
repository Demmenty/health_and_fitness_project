from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect


def registration(request):
    """Обработка запроса регистрации пользователя"""

    if request.method == "POST":
        # проверка соответствия требованиям
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                request.POST["username"], password=request.POST["password1"]
            )
            user.save()
            login(request, user)
            result = "успешный успех"
        else:
            result = form.errors

        data = {
            "result": result,
        }
        return JsonResponse(data, status=200)

    else:
        return redirect("homepage")


def loginuser(request):
    """Обработка запроса входа пользователя"""

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            result = "Пароль или логин введены неверно"
            data = {
                "result": result,
            }
            return JsonResponse(data, status=200)
        else:
            login(request, user)
            result = "доступ разрешен"
            data = {
                "result": result,
            }
            return JsonResponse(data, status=200)
    else:
        return redirect("homepage")


@login_required
def logoutuser(request):
    """Обработка запроса выхода пользователя"""

    if request.method == "POST":
        logout(request)

    return redirect("homepage")
