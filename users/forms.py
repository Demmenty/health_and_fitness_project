from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from users.models import User


class UserLoginForm(AuthenticationForm):
    """The form for logging in"""

    username = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "autocomplete": "username",
                "maxlength": 50,
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pe-5",
                "autocomplete": "current-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password")


class ClientRegistrationForm(UserCreationForm):
    """The form for registration of a client"""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        strip=False,
    )
    password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "d-none"}),
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class PasswordResetForm(PasswordResetForm):
    """The form for password reset"""

    email = forms.EmailField(
        label="Адрес электронной почты:",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}
        ),
    )


class SetPasswordForm(SetPasswordForm):
    """The form for setting new password"""

    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control pe-5",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control pe-5",
            }
        ),
    )


class PasswordChangeForm(PasswordChangeForm):
    """The form for changing password"""

    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control pe-5",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control pe-5",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control pe-5",
            }
        ),
    )
