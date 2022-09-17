from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from personalpage.models import Questionary
from personalpage.forms import QuestionaryForm

# Create your views here.
def controlpage(request):
    """Личный кабинет Параболы"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # список зарегистрированных клиентов
    clients = User.objects.exclude(username='Demmenty').exclude(username='Parrabolla')

    data = {
        'clients': clients,
    }
    return render(request, 'controlpage/controlpage.html', data)



def clientpage(request):
    """Страница контроля за клиентом"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']

    # существоВание анкеты
    try:
        questionary = Questionary.objects.get(user_id=client_id)
    except Questionary.DoesNotExist:
        questionary = ''

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'questionary': questionary,
    }
    return render(request, 'controlpage/clientpage.html', data)



def client_questionary(request):
    """Анкета клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']

    questionary = Questionary.objects.get(user=client_id)
    form = QuestionaryForm()
    
    data = {
        'clientname': clientname,
        'questionary': questionary,
        'form': form,
    }
    return render(request, 'controlpage/client_questionary.html', data)
