from django.shortcuts import render, redirect
from .models import Measurement
from .forms import MeasurementForm
from datetime import date, timedelta, datetime

weekday_dict = {
    0: ['Понедельник', 'ПН'],
    1: ['Вторник', 'ВТ'],
    2: ['Среда', 'СР'],
    3: ['Четверг', 'ЧТ'],
    4: ['Пятница', 'ПТ'],
    5: ['Суббота', 'СБ'],
    6: ['Воскресенье', 'ВС'] }

def make_weekcalendar():
    #создает актуальный календарь на 7 прошедших дней
    week_calendar = {}
    today = date.today()
    days_range = 6

    for _ in range(7):
        selected_date = today - timedelta(days=days_range)
        weekday_short = weekday_dict[selected_date.weekday()][1]
        day_value = weekday_short + ' - ' + str(selected_date.day)
        selected_date = selected_date.strftime('%d.%m.%Y')
        week_calendar[selected_date] = day_value
        days_range -= 1

    return week_calendar


# Create your views here.
def personalpage(request):

    if request.user.is_anonymous:
        return redirect('loginuser')

    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
    else:
        today_measure = ''

    #измерения за неделю
    week_set = Measurement.objects.filter(user=request.user)
    data = {
        'today_measure': today_measure,
        'week_set': week_set,
    }
    return render(request, 'personalpage/personalpage.html', data)

#добавить проверку на то, была ли запись с этой датой
#если была - редактировать её
def addmeasure(request):

    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
        measure_form = MeasurementForm(instance=today_measure)
    else:
        measure_form = MeasurementForm()

    if request.method == 'GET':
        week_calendar = make_weekcalendar()
        data = {
            'measure_form': measure_form,
            'error': '',
            'week_calendar': week_calendar,
            }
        return render(request, 'personalpage/addmeasure.html', data)
    
    if request.method == 'POST':

        if today_set:
            form = MeasurementForm(request.POST, instance=today_measure) 
        else:
            form = MeasurementForm(request.POST)    

        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = request.user
            weekday_number = newform.date.weekday()
            newform.weekday = weekday_dict[weekday_number][0]
            form.save()
            return redirect('personalpage')
        else:
            week_calendar = make_weekcalendar()
            data = {
                'measure_form': measure_form,
                'error': 'Данные введены некорректно. Попробуйте ввести их еще раз.',
                'week_calendar': week_calendar,
                }
            return render(request, 'personalpage/addmeasure.html', data)
