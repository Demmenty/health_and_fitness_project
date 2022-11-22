from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse

# Create your views here.
def homepage(request):

    data = {
        'registration_form': UserCreationForm(),
        'login_form': AuthenticationForm,
        }

    return render(request, 'homepage/homepage.html', data)


def registration(request):

    if request.method == 'POST':
        # проверка соответствия требованиям
        form = UserCreationForm(request.POST)
        if form.is_valid():

            user = User.objects.create_user(request.POST['username'],
                                            password=request.POST['password1'])
            user.save()
            login(request, user)
            result = 'успешный успех'
        else:
            result = form.errors

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)

    else:
        return redirect('homepage')


def loginuser(request):
        
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            result = 'Пароль или логин введены неверно'
            data = {
                'result': result,
            }
            return JsonResponse(data, status=200)
        else:
            login(request, user)
            result = 'доступ разрешен'
            data = {
                'result': result,
            }
            return JsonResponse(data, status=200)
    else:
        return redirect('homepage')


def logoutuser(request):

    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    else:
        return redirect('homepage')