from django.shortcuts import render, redirect
from .models import Measurement, Questionary, FatSecretEntry
from .forms import MeasurementForm, QuestionaryForm
from datetime import date, datetime, timedelta
from fatsecret import Fatsecret

WEEKDAY_RU = {
    0: ['Понедельник', 'ПН'],
    1: ['Вторник', 'ВТ'],
    2: ['Среда', 'СР'],
    3: ['Четверг', 'ЧТ'],
    4: ['Пятница', 'ПТ'],
    5: ['Суббота', 'СБ'],
    6: ['Воскресенье', 'ВС'] }

def make_weekcalendar():
    """Генерация календаря на неделю для выбора даты"""
    week_calendar = {}
    for i in range(7):
        selected_date = date.today() - timedelta(days=(6-i))
        weekday_short = WEEKDAY_RU[selected_date.weekday()][1]
        day_value = weekday_short + ' - ' + str(selected_date.day)
        week_calendar[selected_date] = day_value

    return week_calendar


def make_weekmeasureforms(request):
    """Генерация списка формочек за неделю"""
    week_measureforms = []
    for i in range(7):
        measure_date = date.today() - timedelta(days=i)
        try:
            # если запись за этот день есть, то формочка создается на ее основе
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)
        except Measurement.DoesNotExist:
            # если записи за этот день нет, то формочка создается пустая
            measure_form = MeasurementForm()
            measure_form = measure_form.save(commit=False)
            # в нее сразу записывается user, дата и день недели
            measure_form.user = request.user
            measure_form.date = measure_date
            measure_form.weekday = WEEKDAY_RU[measure_date.weekday()][0]
            # сохраняется запись в базе
            measure_form.save()
            # и формочка создается на основе этой записи
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)      
        week_measureforms.append(measure_form)

    return week_measureforms


# My views
def personalpage(request):
    """Личный кабинет клиента"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # анкета
    try:
        questionary_existing = Questionary.objects.get(user=request.user)
    except Questionary.DoesNotExist:
        questionary_existing = ''

    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
    else:
        today_measure = ''

    #измерения за неделю
    week_set = reversed(Measurement.objects.filter(user=request.user)[:7])

    # словарь по видам данных для красивой таблички
    week_data = {'date': [],
                 'weekday': [],
                 'feel': [],
                 'weight': [],
                 'fat': [],
                 'pulse': [],
                 'pressure': [],
                 'comment': []}

    for measure in week_set:
        week_data['date'].append(measure.date)
        week_data['weekday'].append(measure.weekday)
        week_data['feel'].append(measure.feel)
        week_data['weight'].append(measure.weight)
        week_data['fat'].append(measure.fat)
        week_data['pulse'].append(measure.pulse)
        if measure.pressure_upper is not None and measure.pressure_lower is not None:
            week_data['pressure'].append(str(measure.pressure_upper) + '/' + str(measure.pressure_lower))
        else:
            week_data['pressure'].append('')
        week_data['comment'].append(measure.comment)
    
    data = {
        'week_data': week_data,
        'today_measure': today_measure,
        'week_set': week_set,
        'questionary_existing': questionary_existing,
    }
    return render(request, 'personalpage/personalpage.html', data)


def questionary(request):
    """Страница заполнения личной анкеты"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # GET-запрос
    if request.method == 'GET':
        # проверяем, есть ли у клиента уже анкета
        try:
            questionary_existing = Questionary.objects.get(user=request.user)
            # создаем форму на ее основе
            form = QuestionaryForm(instance=questionary_existing)
        except Questionary.DoesNotExist:
             # или создаем пустую форму
            form = QuestionaryForm()

        # рендерим страницу с формой
        data = {
            'form': form,
            'error': '',
        }
        return render(request, 'personalpage/questionary.html', data)

    # POST-запрос
    if request.method == 'POST':
        # получаем форму из запроса
        form = QuestionaryForm(request.POST)
        # проверяем на корректность
        if form.is_valid():
            try:
                # пробуем получить анкету из БД
                questionary_existing = Questionary.objects.get(user=request.user)
                form = QuestionaryForm(request.POST, instance=questionary_existing)
                form.save()
                return redirect('personalpage')
            except Questionary.DoesNotExist:
                # если ее нет - сохраняем как новую
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect('personalpage')
        # если форма некорректна - перезагружаем страницу с ошибкой
        else:
            # проверяем, есть ли у клиента уже анкета
            try:
                questionary_existing = Questionary.objects.get(user=request.user)
                # создаем форму на ее основе
                form = QuestionaryForm(instance=questionary_existing)
            except Questionary.DoesNotExist:
                # или создаем пустую форму
                form = QuestionaryForm()
            data = {
                'form': form,
                'error': 'Данные введены некорректно. Попробуйте ещё раз.',
            }
            return render(request, 'personalpage/questionary.html', data)


def addmeasure(request):
    """Страница внесения и редактирования измерений"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # генерация календарика и формочек на 7 дней
    week_measureforms = make_weekmeasureforms(request)
    week_calendar = make_weekcalendar()
    
    # GET-запрос
    if request.method == 'GET':
        data = {
            'week_measureforms': week_measureforms,
            'error': '',
            'week_calendar': week_calendar,
            }
        return render(request, 'personalpage/addmeasure.html', data)

    # POST-запрос
    if request.method == 'POST':
        # получаем форму из запроса
        form = MeasurementForm(request.POST)
        # проверяем на корректность
        if form.is_valid():
            # получаем дату из формы
            measure_date = form.cleaned_data['date']
            try:
                # получаем запись из БД с этим числом
                measure = Measurement.objects.get(date=measure_date, user=request.user) 
                # сформируем форму на ее основе и перезаписываем
                form = MeasurementForm(request.POST, instance=measure)
                form.save()
                return redirect('personalpage')
            # если записи за число нет - это странно
            except Measurement.DoesNotExist:
                # перезагружаем с ошибкой
                data = {
                'week_measureforms': week_measureforms,
                'error': 'Случилось что-то непонятное, либо вы читерите :(',
                'week_calendar': week_calendar,
                }
                return render(request, 'personalpage/addmeasure.html', data)
        # если форма некорректна - перезагружаем страницу с ошибкой
        else:
            data = {
                'week_measureforms': week_measureforms,
                'error': 'Данные введены некорректно. Попробуйте ввести их еще раз.',
                'week_calendar': week_calendar,
                }
            return render(request, 'personalpage/addmeasure.html', data)


# данные fatsecret
consumer_key = '96509fd6591d4fb384386e1b75516777'
consumer_secret = 'cb1398ad47344691b092cabce5647116'
fs = Fatsecret(consumer_key, consumer_secret)


def mealjournal(request):
    """Страница контроля питания и кбжу"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # GET-запрос
    if request.method == 'GET':

        # проверка подключения Fatsecret к этому аккаунту
        try:
            userdata = FatSecretEntry.objects.get(user=request.user)
            session_token = (userdata.oauth_token, userdata.oauth_token_secret)

            fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)

            # данные для тех, у кого подключен FatSecret
            user_not_connected = False  
            profile_info = fs.profile_get()
            food_entries_month = fs.food_entries_get_month(date=datetime.today())

        except FatSecretEntry.DoesNotExist:
            
            # данные для тех, у кого НЕ подключен FatSecret
            user_not_connected = True
            profile_info = 'Нет данных'
            food_entries_month = 'Нет данных'


        data = {
            'profile_info': profile_info,
            'food_entries_month': food_entries_month,
            'user_not_connected': user_not_connected,
        }
        return render(request, 'personalpage/mealjournal.html', data)



def fatsecretauth(request):
    """Подключение к FatSecret"""

    if request.GET.get('oauth_verifier', None):

        # получаем данные от response FatSecret
        verifier_pin = request.GET.get('oauth_verifier')
        oauth_token = request.GET.get('oauth_token')

        # Сеанс теперь аутентифицирован
        session_token = fs.authenticate(verifier_pin)

        # записываем данные для сессии в базу
        FatSecretEntry.objects.create(user=request.user, oauth_token=session_token[0], oauth_token_secret=session_token[1])

        return redirect('mealjournal')

    else:
        # получаем адрес подключения и направляем по нему
        auth_url = fs.get_authorize_url(callback_url="http://127.0.0.1:8000/personalpage/fatsecretauth/")

        # получаем oauth_token и oauth_verifier
        # каждый раз разные
        return redirect(auth_url)