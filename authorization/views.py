from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def registration(request):

    data = {
        'form': UserCreationForm(),
        'error': '',
        }

    if request.method == 'GET':     
        return render(request, 'authorization/registration.html', data)
        
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('personalpage')
            except IntegrityError:
                data['error'] = 'К сожалению, это имя уже занято :('
                return render(request, 'authorization/registration.html', data)
        else:
            data['error'] = 'Пароли не совпадают!'
            return render(request, 'authorization/registration.html', data)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')


def loginuser(request):

    data = {
        'form': AuthenticationForm,
        'error': '',
        }

    if request.method == 'GET':     
        return render(request, 'authorization/loginuser.html', data)
        
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            data['error'] = 'Пароль или имя введены неверно'
            return render(request, 'authorization/loginuser.html', data)
        else:
            login(request, user)
            return redirect('personalpage')
