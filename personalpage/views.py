from django.shortcuts import render, redirect
from .models import Measurement
from .forms import MeasurementForm
from datetime import date, timedelta

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
        # selected_date = selected_date.strftime('%Y-%m-%d')
        week_calendar[selected_date] = day_value
        days_range -= 1

    return week_calendar


# My views
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


def addmeasure(request):




    if request.method == 'GET':

        #делаем список из форм от записей за неделю (либо пустых)
        week_measureforms = []
        for i in range(7):
            measure_date = date.today() - timedelta(days=i)
            try:
                measure = Measurement.objects.get(date=measure_date, user=request.user)
                measure_form = MeasurementForm(instance=measure)
            except Measurement.DoesNotExist:
                measure_form = MeasurementForm()
                measure_form = measure_form.save(commit=False)
                measure_form.user = request.user
                measure_form.date = measure_date
                weekday_number = measure_form.date.weekday()
                measure_form.weekday = weekday_dict[weekday_number][0]
                measure_form.save()

                measure = Measurement.objects.get(date=measure_date, user=request.user)
                measure_form = MeasurementForm(instance=measure)
                
            week_measureforms.append(measure_form)


        week_calendar = make_weekcalendar()
        data = {
            'week_measureforms': week_measureforms,
            'error': '',
            'week_calendar': week_calendar,
            }
        return render(request, 'personalpage/addmeasure.html', data)

    
    if request.method == 'POST':
        # получаем форму из запроса
        form = MeasurementForm(request.POST)
        # проверяем на корректность
        if form.is_valid():
            # получаем введенную дату
            measure_date = form.cleaned_data['date']
            # пробуем получить запись за это число
            # сформировать форму на ее основе
            # и перезаписать
            try:
                measure = Measurement.objects.get(date=measure_date, user=request.user)
                form = MeasurementForm(request.POST, instance=measure)
                form.save()
                return redirect('personalpage')
            # если записи за число нет
            except Measurement.DoesNotExist:
                # делаем новую запись
                # добавляя недостающие данные
                newform = form.save(commit=False)
                newform.user = request.user
                weekday_number = newform.date.weekday()
                newform.weekday = weekday_dict[weekday_number][0]
                newform.save()
                return redirect('personalpage')

        # если форма неккоректна
        # генерируем ту же страницу
        # как в GET но с ошибкой

        # дополнить!
        else:
            week_calendar = make_weekcalendar()
            data = {
                'week_measureforms': week_measureforms,
                'error': 'Данные введены некорректно. Попробуйте ввести их еще раз.',
                'week_calendar': week_calendar,
                }
            return render(request, 'personalpage/addmeasure.html', data)
