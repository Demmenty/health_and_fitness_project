from django import forms
from django.contrib.auth.forms import UserCreationForm


class ClientRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя клиента",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
