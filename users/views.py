from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, QueryDict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from config.settings import DOMAIN
from expert.decorators import expert_required
from main.utils import is_ajax
from users.forms import (
    ClientRegistrationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from users.models import User


@expert_required
@require_http_methods(["POST"])
def register_client(request):
    """
    Registers a new client with the provided data by expert.
    Sends an email to the client with the registration information.

    Args:
        request: The HTTP request object containing the client registration data.

    Returns:
        If the registration form is valid, an empty HTTP response indicating success.
        If the registration form is invalid, a JSON response containing the form errors with a status code of 400.
    """

    request.POST = QueryDict(request.POST.urlencode(), mutable=True)
    request.POST["email"] = request.POST["email"].lower()
    form = ClientRegistrationForm(request.POST)

    if form.is_valid():
        client = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        client.save()
        client.email_user(
            subject=f"Регистрация на {DOMAIN}",
            message=(
                f"Добрый день,\n\n"
                f"Ваш аккаунт на сервисе {DOMAIN} успешно зарегистрирован.\n\n"
                f"Ваш логин: {form.cleaned_data['username']}\n"
                f"Ваш пароль: {form.cleaned_data['password1']}\n\n"
                f"С уважением,\n"
                f"Команда Fullstack Fitness"
            ),
        )
        return HttpResponse("ОK")
    else:
        return JsonResponse(form.errors, status=400)


@require_http_methods(["POST"])
def login_user(request):
    """
    Login a user with provided credentials and return a JSON response.

    Parameters:
        `request`: The HTTP request object.
    Returns:
        A JSON response containing the next redirect link.
    Raises:
        HttpResponseForbidden: If the provided credentials are invalid.
    """

    user: User = authenticate(
        request,
        username=request.POST.get("username"),
        password=request.POST.get("password"),
    )
    if not user:
        return HttpResponseForbidden("Пароль или логин введены неверно")

    login(request, user)

    if user.is_expert:
        redirect_link = reverse_lazy("expert:clients")
    else:
        redirect_link = reverse_lazy("client:profile")

    data = {"next": redirect_link}
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def logout_user(request):
    """
    Logs out the user and redirects to the home page.

    Parameters:
        request: the HTTP request object
    Return:
        None
    """

    logout(request)

    return redirect("main:home")


class PasswordReset(auth_views.PasswordResetView):
    """Password reset view class."""

    form_class = PasswordResetForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset_done")
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    """Password reset confirm view class."""

    form_class = SetPasswordForm
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetDone(auth_views.PasswordResetDoneView):
    """Password reset done view class."""

    template_name = "users/password_reset_done.html"


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    """Password reset complete view class."""

    template_name = "users/password_reset_complete.html"


class PasswordChange(auth_views.PasswordChangeView):
    """Password change view class."""

    form_class = PasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change_done")


class PasswordChangeDone(auth_views.PasswordChangeDoneView):
    """Password change done view class."""

    template_name = "users/password_change_done.html"


def csrf_failure(request, reason=""):
    """
    Check if the CSRF verification failed and handle the failure accordingly.

    Args:
        request: The HTTP request object.
        reason (optional): The reason for the CSRF failure.
    Returns:
        If the request is an AJAX request, returns an HttpResponseForbidden with the message "CSRF проверка не пройдена".
        Otherwise, redirects the user to the "main:home" URL.
    """

    if is_ajax(request):
        return HttpResponseForbidden("CSRF проверка не пройдена")

    return redirect("main:home")
