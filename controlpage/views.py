from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def controlpage(request):
    """Личный кабинет Параболы"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # если не Парабола - перенаправление на домашнюю
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # список зарегистрированных клиентов
    clients = User.objects.exclude(username='Demmenty').exclude(username='Parrabolla')

    data = {
        'clients': clients,
    }

    return render(request, 'controlpage/controlpage.html', data)
