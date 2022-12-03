from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from controlpage.forms import ConsultationsignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def saveConsultationSignup(request):
    """Сохранение формы заявки на консультацию через аякс
       Используется в homepage/homepage.html
    """
    if request.method == 'POST':
        form = ConsultationsignupForm(request.POST)
        if form.is_valid():
            form.save()
            result = 'Заявка получена'
        else:
            result = form.errors

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)

    else:
        return redirect('homepage')



# Create your views here.
def homepage(request):
    """Главная страница сайта"""
    data = {
        'registration_form': UserCreationForm(),
        'login_form': AuthenticationForm,
        'consultation_form': ConsultationsignupForm(),
        }

    return render(request, 'homepage/homepage.html', data)


def registration(request):
    """Обработка запроса регистрации пользователя"""
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
    """Обработка запроса входа пользователя"""
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
    """Обработка запроса выхода пользователя"""
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    else:
        return redirect('homepage')