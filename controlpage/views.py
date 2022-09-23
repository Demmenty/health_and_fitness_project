from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from personalpage.models import Measurement, Questionary
from personalpage.forms import QuestionaryForm
from datetime import date
from personalpage.views import make_avg_for_period


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

    # измерения за сегодня
    try:
        today_measure = Measurement.objects.get(date__exact=date.today(), user_id=client_id)
        if (today_measure.feel is None and today_measure.weight is None and
            today_measure.fat is None and today_measure.pulse is None and
            (today_measure.pressure_upper is None or today_measure.pressure_lower is None) and
            today_measure.calories is None and today_measure.comment == "") :
            today_measure = ''
    except Measurement.DoesNotExist:
        today_measure = ''

    # измерения за неделю
    week_measures = Measurement.objects.filter(user=client_id)[:7]
    # средние значения измерений за неделю 
    avg_week = make_avg_for_period(client_id, period=7)
    # измерялось ли давление (отображать или нет)
    show_pressure_week = False
    if any(day.pressure_upper for day in week_measures):
        show_pressure_week = True
    


    data = {
        'clientname': clientname,
        'client_id': client_id,
        'questionary': questionary,
        'today_measure': today_measure,
        'week_measures': week_measures,
        'avg_week': avg_week,
        'show_pressure_week': show_pressure_week,
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
