from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def homepage(request):

    data = {
        'registration_form': UserCreationForm(),
        'login_form': AuthenticationForm,
        'error': '',
        }

    return render(request, 'homepage/homepage.html', data)


def registration(request):
        
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('personalpage')
            except IntegrityError:
                error = 'К сожалению, это имя уже занято :('
        else:
            error = 'Пароли не совпадают!'

        data = {
            'error': error,
        }
        return render(request, 'homepage/homepage.html', data)


def loginuser(request):
        
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = 'Пароль или имя введены неверно'
            data = {
                'error': error,
            }
            return render(request, 'homepage/homepage.html', data)
        else:
            login(request, user)
            return redirect('personalpage')


def logoutuser(request):

    if request.method == 'POST':
        logout(request)
        return redirect('homepage')