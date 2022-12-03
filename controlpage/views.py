import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from personalpage.models import Measurement, Questionary, FatSecretEntry, Anthropometry, UserSettings, MeasureColorField
from controlpage.models import Commentary, Consultationsignup
from personalpage.forms import QuestionaryForm
from controlpage.forms import MeasureColorFieldForm, CommentaryForm
from time import sleep
from itertools import zip_longest
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from personalpage.views import make_avg_for_period
from fatsecret import Fatsecret, GeneralError
from django.http import JsonResponse


# данные fatsecret - засунуть в бд!!!
consumer_key = '96509fd6591d4fb384386e1b75516777'
consumer_secret = 'cb1398ad47344691b092cabce5647116'
fs = Fatsecret(consumer_key, consumer_secret)


def make_session(user):
    """создание сессии с FatSecret Api для переданного пользователя"""
    global fs
    userdata = FatSecretEntry.objects.get(user=user)
    session_token = (userdata.oauth_token, userdata.oauth_token_secret)
    fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)


def get_noun_ending(number, one, two, five):
    """Функция возвращает вариант слова с правильным окончанием
       в зависимости от числа
       Нужно передать число и соответствующие варианты
       например: get_noun_ending(4, 'слон', 'слона', 'слонов'))
    """
    n = abs(number)
    n %= 100
    if 20 >= n >= 5:
        return five
    n %= 10
    if n == 1:
        return one
    if 4 >= n >= 2:
        return two
    return five


def get_client_contacts(client_id):
    """Достаем контакты клиента из его настроек"""
    try:
        instance = UserSettings.objects.get(user_id=client_id)

        fields = [
            'telegram',
            'whatsapp',
            'discord',
            'skype',
            'vkontakte',
            'facebook',
        ]

        for field in fields: 
            if getattr(instance, field):
                client_contacts = {}
                for f in fields:
                    client_contacts[f] = getattr(instance, f)
                client_contacts['preferred'] = getattr(instance, 'preferred_contact')

                return client_contacts

        return False

    except UserSettings.DoesNotExist:
        return False


def today_commentary_form(client_id):
    """Получение формы для комплексного комментария клиенту от эксперта
       Дата - сегодняшняя, на другие даты меняется на странице скриптом
    """
    try:
        instance = Commentary.objects.get(client=client_id, date=date.today())
        form = CommentaryForm(instance=instance)
    except Commentary.DoesNotExist:
        form = CommentaryForm()

    return form


def get_commentary_form(request):
    """Получение формы коммента клиенту для эксперта
       для выбранной на странице даты через скрипт в layout"""

    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.GET.get('client_id', None)

    comment_date = request.GET['date']

    try:
        instance = Commentary.objects.get(client=client_id, date=comment_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
        }
    except Commentary.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        }

    return JsonResponse(data, status=200)


def save_commentary_form(request):
    """Сохранение формы коммента для клиента через аякс-скрипт
       Используется в controlpage/layout.html
    """

    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':

        client_id = request.POST['client']
        form = CommentaryForm(request.POST)

        if form.is_valid():
            comment_date = form.cleaned_data['date']

            try:
                instance = Commentary.objects.get(client=client_id, date=comment_date)
                form = CommentaryForm(request.POST, instance=instance)
                form = form.save(commit=False)
            except Commentary.DoesNotExist:
                form = form.save(commit=False)
                form.client_id = client_id

            # если поле не пусто, то оставить флаг о непрочитанности
            form.general_read = not bool(form.general)
            form.measurements_read = not bool(form.measurements)
            form.nutrition_read = not bool(form.nutrition)
            form.workout_read = not bool(form.workout)

            form.save()
            result = 'комментарий сохранен'
        
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)


# My views

def controlpage(request):
    """Личный кабинет Параболы"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # список зарегистрированных клиентов
    # !!! clients = User.objects.exclude(username='Demmenty').exclude(username='Parrabolla')
    clients = User.objects.exclude(username='Parrabolla')
    # новые заявки на консультацию
    new_consult_requests = Consultationsignup.objects.filter(is_read=0)
    new_consult_requests_count = new_consult_requests.count()

    data = {
        'clients': clients,
        'new_consult_requests_count': new_consult_requests_count,
    }
    return render(request, 'controlpage/controlpage.html', data)


def consult_requests(request):
    """Управление заявками на консультацию"""
    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # заявки на консультацию
    consult_requests = Consultationsignup.objects.all()
    # новые заявки на консультацию
    new_consult_requests = Consultationsignup.objects.filter(is_read=0)
    new_consult_requests_count = new_consult_requests.count()

    data = {
            'consult_requests': consult_requests,
            'new_consult_requests_count': new_consult_requests_count,
        }
    return render(request, 'controlpage/consult_requests.html', data)


def clientpage(request):
    """Страница контроля за клиентом"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)
    # дата регистрации
    date_joined = User.objects.get(username=clientname).date_joined.date()

    # существоВание анкеты
    try:
        questionary = Questionary.objects.get(user_id=client_id)
    except Questionary.DoesNotExist:
        questionary = ''

    # проверка подключения FatSecret
    try:
        make_session(client_id)
        fs_connected = True
    except FatSecretEntry.DoesNotExist:
        fs_connected = False

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

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'questionary': questionary,
        'fs_connected': fs_connected,
        'today_measure': today_measure,
        'date_joined': date_joined,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/clientpage.html', data)


def client_measurements(request):
    """Страница отслеживания ежедневных измерений"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)

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
    
    # статистика за выбранный период
    show_pressure_period = False
    if request.GET.get('selectperiod'):
        selected_period = int(request.GET.get('selectperiod'))
        # средние значения измерений за произвольный период
        avg_period = make_avg_for_period(client_id, period=selected_period)
        # список измерений за этот период
        period = Measurement.objects.filter(user=client_id)[:selected_period]
        # измерялось ли давление (отображать или нет)
        if any(day.pressure_upper for day in period):
            show_pressure_period = True
        # красивый формат
        selected_period = str(selected_period) + " " + get_noun_ending(selected_period, 'день', 'дня', 'дней')
    else:
        selected_period = ""
        avg_period = ""
        period = ""

    # наличие цветовых настроек для клиента
    colorset_exist = bool(MeasureColorField.objects.filter(user_id=client_id))

    # настройки цветовых фонов для показателей клиента
    colorset_forms = []
    if colorset_exist:
        for index_id in range(1, 11):
            for color_id in range(2, 7):
                instance = MeasureColorField.objects.get(
                    user_id=client_id,
                    index_id=index_id,
                    color_id=color_id
                    )
                form = MeasureColorFieldForm(instance=instance)
                colorset_forms.append(form)
    else:
        for index_id in range(1, 11):
            for color_id in range(2, 7):
                form = MeasureColorFieldForm(initial={
                    'user': client_id,
                    'index': index_id,
                    'color': color_id
                    })
                colorset_forms.append(form)

    # указанное в анкете нормальное давление
    try:
        norm_pressure = Questionary.objects.get(user=client_id).norm_pressure
        if norm_pressure == 'no':
            norm_pressure = 'не знает'
    except Questionary.DoesNotExist:
        norm_pressure = 'не заполнено'

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'today_measure': today_measure,
        'week_measures': week_measures,
        'selected_period': selected_period,
        'period': period,
        'avg_week': avg_week,
        'avg_period': avg_period,
        'show_pressure_week': show_pressure_week,
        'show_pressure_period': show_pressure_period,
        'colorset_exist': colorset_exist,
        'colorset_forms': colorset_forms,
        'norm_pressure': norm_pressure,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_measurements.html', data)


def color_settings_save(request):
    """Сохранение настроек цветов для показателей клиента через ajax"""

    if request.user.username != 'Parrabolla':
        data = {'status': 'No!'}
        return JsonResponse(data, status=403)

    if request.method == 'POST':

        client_id = request.POST['client_id']
        indices = request.POST.getlist('index')
        colors = request.POST.getlist('color')
        low_limits = request.POST.getlist('low_limit')
        up_limits = request.POST.getlist('upper_limit')

        values = zip_longest(indices, colors, low_limits, up_limits)

        # наличие цветовых настроек для клиента
        colorset_exist = bool(MeasureColorField.objects.filter(user_id=client_id))

        if colorset_exist:
            for index, color, low, up in values:
                if not low:
                    low = None
                if not up:
                    up = None
                instance = MeasureColorField.objects.filter(
                    user_id=client_id,
                    index_id=index,
                    color_id=color)
                instance.update(low_limit=low, upper_limit=up)

        else:
            for index, color, low, up in values:
                if not low:
                    low = None
                if not up:
                    up = None
                MeasureColorField.objects.create(
                    user_id=client_id,
                    index_id=index, 
                    color_id=color, 
                    low_limit=low, 
                    upper_limit=up)

        data = {}
        return JsonResponse(data, status=200)


def color_settings_send(request):
    """Отправка текущих настроек цветов показателей"""
    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    
    client_id = request.GET['client_id']
    if client_id == 'user':
        client_id = request.user

    colorset = MeasureColorField.objects.filter(user_id=client_id).order_by('index', 'color')
    
    if colorset:
        data = {'feel': {},
                'weight': {},
                'fat': {},
                'pulse': {},
                'pressure_upper': {},
                'pressure_lower': {},
                'calories': {},
                'protein': {},
                'fats': {},
                'carbohydrates': {},
                }
        for object in colorset:
            data[str(object.index)][str(object.color.id)] = {
                                                'color': str(object.color),
                                                'low': str(object.low_limit),
                                                'up': str(object.upper_limit) }
    else:
        data = {}

    return JsonResponse(data, status=200)



def client_questionary(request):
    """Анкета клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)

    # ???
    questionary = Questionary.objects.get(user=client_id)
    form = QuestionaryForm()
    
    data = {
        'clientname': clientname,
        'client_id': client_id,
        'questionary': questionary,
        'form': form,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_questionary.html', data)



def client_mealjournal(request):
    """Страница контроля питания и кбжу клиента
    Тут отображается таблица за сегодняшний день
    и таблица за текущий месяц
    """
    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)
    # для поля выбора
    today_day = str(date.today())
    previous_month = str(date.today() + relativedelta(months=-1))[0:7]
    
    # проверка на интеграцию с FatSecret
    try:
        make_session(client_id)
        client_connected = True
    except FatSecretEntry.DoesNotExist:
        client_connected = False
        data = {
            'clientname': clientname,
            'client_id': client_id,
            'client_connected': client_connected,
            'today_day': today_day,
            'previous_month': previous_month,
            'client_contacts': client_contacts,
            'client_comment_form': client_comment_form,
        }
        return render(request, 'controlpage/client_mealjournal.html', data)  

    # открываем сохраненные данные о продуктах из файла
    with open('personalpage/food_cache.pickle', 'rb') as file:
        food_cache = pickle.load(file)
    # продукты, для которых нет инфо о граммовке порции
    prods_without_info = {}

    # ПИТАНИЕ ЗА СЕГОДНЯ
    food_entry = fs.food_entries_get(date=datetime.today())

    # категории для таблички
    count_meal_in_category = {
        'Breakfast': 0,
        'Lunch': 0,
        'Dinner': 0,
        'Other': 0,
    }
    # итоговые кбжу дня
    day_total = {
            'amount': 0,
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbohydrate': 0,
            }

    # обработка каждой записи о продукте
    for food in food_entry:

        # подсчет количеств блюд для каждой категории для таблички
        count_meal_in_category[food['meal']] += 1

        # получение инфы об этом продукте
        temp_food_cache = {}
            # сначала в кеше
        if food_cache.get(food['food_id']):
            food_info = food_cache[food['food_id']]
        else:
            # потом в FatSecret
            # добавить обработчик ошибки! (с таймером - если много запросов)
            food_info = fs.food_get(food_id=food['food_id'])
            sleep(2)

            # обработка для компактного сохранения
            if type(food_info['servings']['serving']) is dict:
                temp_food_cache[food_info['food_id']] = {
                    'food_name': food_info['food_name'],
                    'servings': {
                        'serving': {
                            'serving_id': food_info['servings']['serving']['serving_id'],
                            'measurement_description': food_info['servings']['serving']['measurement_description'],
                            'metric_serving_amount': food_info['servings']['serving'].get('metric_serving_amount', None),
                            'number_of_units': food_info['servings']['serving']['number_of_units'],
                            'metric_serving_unit': food_info['servings']['serving'].get('metric_serving_unit', None),
                            'serving_description': food_info['servings']['serving']['serving_description'] }}}
            else:
                temp_food_cache[food_info['food_id']] = {
                    'food_name': food_info['food_name'],
                    'servings': {
                        'serving': [] }}
                for dic in food_info['servings']['serving']:
                    temp_food_cache[food_info['food_id']]['servings']['serving'].append({
                        'serving_id': dic['serving_id'],
                        'measurement_description': dic['measurement_description'],
                        'metric_serving_amount': dic.get('metric_serving_amount', None),
                        'number_of_units': dic['number_of_units'],
                        'metric_serving_unit': dic.get('metric_serving_unit', None),
                        'serving_description': dic['serving_description'] })

            # сохранение в кеш
            food_cache.update(temp_food_cache)


        # добавление инфы в food для соответствующего вида порции
        if type(food_info['servings']['serving']) is list:
            for serv_info in food_info['servings']['serving']:
                if serv_info['serving_id'] == food['serving_id']:
                    food['serving'] = serv_info
                    break
        else:
            food['serving'] = food_info['servings']['serving']

        # добавляем нормальное отображение количества
        # если измерение в г или мл - считаем как есть
        if (food['serving']['measurement_description'] == 'g' or
            food['serving']['measurement_description'] == 'ml'):
            food['norm_amount'] = int(float(food['number_of_units']))
            day_total['amount'] += food['norm_amount']
        else:
            # если измерение в порциях - сначала проверяем, есть ли граммовка порции
            if food['serving'].get('metric_serving_amount') is None:
                # если в инфе не оказалось граммовки порции
                # добавляем эту еду в спец.словарь и не считаем amount
                prods_without_info[food['food_id']] = {
                    'food_entry_name': food['food_entry_name'],
                    'serving_description': food['serving'].get('serving_description', 'порция'),
                    'serving_id': food['serving_id'],
                    'calories_per_serving': food['serving'].get('calories', food['calories']) }
            else:
                # если в инфе метрика есть - считаем и добавляем к общему подсчету
                food['norm_amount'] = int(float(food['number_of_units']) *
                                        float(food['serving']['metric_serving_amount']) *
                                        float(food['serving']['number_of_units']))
                day_total['amount'] += food['norm_amount']

        # подсчет итоговой суммы кбжу
        day_total['calories'] += int(food['calories'])
        day_total['protein'] += float(food['protein'])
        day_total['fat'] += float(food['fat'])
        day_total['carbohydrate'] += float(food['carbohydrate'])

    # записываем измененный кеш обратно в файл
    with open('personalpage/food_cache.pickle', 'wb') as f:
        pickle.dump(food_cache, f)
        
    # нумерация продуктов без инфы о порции
    index_number = 1
    for prod in prods_without_info:
        prods_without_info[prod]['index_number'] = index_number
        index_number += 1

    # округляем результаты в получившемся итоге по кбжу
    for key, value in day_total.items():
        day_total[key] = round(value, 2)


    # ПИТАНИЕ ЗА ТЕКУЩИЙ МЕСЯЦ
    # средние кбжу
    avg_month = {
        'protein': 0,
        'fat': 0,
        'carbo': 0,
        'calories': 0
    }
    try:
        food_entries_month = fs.food_entries_get_month(date=datetime.today())
        # если за месяц одна запись - будет просто словарь
        if type(food_entries_month) is dict:
            food_entries_month['date_int'] = (date(1970, 1, 1) + 
                            timedelta(days=int(food_entries_month['date_int'])))
            avg_month['protein'] = food_entries_month['protein']
            avg_month['fat'] = food_entries_month['fat']
            avg_month['carbo'] = food_entries_month['carbohydrate']
            avg_month['calories'] = food_entries_month['calories']
            # превращаем в список из словаря, чтобы табличка не ебнулась
            food_entries_month = [food_entries_month]
        else:
            # если за день нет записей - то она итак не отображается (поэтому тут другая формула)
            days_count = len(food_entries_month)
            for day in food_entries_month:
                day['date_int'] = date(1970, 1, 1) + timedelta(days=int(day['date_int']))
                avg_month['protein'] += float(day['protein'])
                avg_month['fat'] += float(day['fat'])
                avg_month['carbo'] += float(day['carbohydrate'])
                avg_month['calories'] += float(day['calories'])
            avg_month['protein'] = round(avg_month['protein'] / days_count, 2)
            avg_month['fat'] = round(avg_month['fat'] / days_count, 2)
            avg_month['carbo'] = round(avg_month['carbo'] / days_count, 2)
            avg_month['calories'] = round(avg_month['calories'] / days_count, 2)

    except KeyError:
        # KeyError = записей нет
        food_entries_month = ""

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'client_connected': client_connected,
        'food_entries_month': food_entries_month,
        'prods_without_info': prods_without_info,
        'avg_month': avg_month,
        'food_entry': food_entry,
        'day_total': day_total,
        'count_meal_in_category': count_meal_in_category,
        'today_day': today_day,
        'previous_month': previous_month,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_mealjournal.html', data)   


def client_foodbydate(request):
    """Получение данных за опр.день из FatSecret
    С ТОПом по количеству и калориям
    """
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)

    # делаем сессию с FatSecret
    make_session(client_id)

    # получаем введенную дату
    briefdate = request.GET.get('date')
    if briefdate is None or not briefdate:
        return redirect('client_mealjournal')
    # форматируем для дальнейшей работы
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")
    # заготовки для html
    prev_date = str(briefdate - timedelta(days=1))[:10]
    next_date = str(briefdate + timedelta(days=1))[:10]

    # добавить обработчик too many actions!?

    # ПИТАНИЕ за выбранную дату (briefdate)
    food_entry = fs.food_entries_get(date=briefdate)
    # ???
    if not food_entry:
        data = {
            'clientname': clientname,
            'client_id': client_id,
            'top_calories': "",
            'top_amount': "",
            'total_by_prod': "",
            'day_total': "",
            'count_meal_in_category': "",
            'prods_without_info': "",
            'briefdate': briefdate,
            'prev_date': prev_date,
            'next_date': next_date,
            'food_entry': food_entry,
            'client_contacts': client_contacts,
            'client_comment_form': client_comment_form,
        }
        return render(request, 'controlpage/client_foodbydate.html', data)

    # открываем сохраненные данные о продуктах из файла
    with open('personalpage/food_cache.pickle', 'rb') as file:
        food_cache = pickle.load(file)


    # продукты, для которых нет инфо о граммовке порции
    prods_without_info = {}
    # категории для таблички
    count_meal_in_category = {
        'Breakfast': 0,
        'Lunch': 0,
        'Dinner': 0,
        'Other': 0,
    }
    # итоговые кбжу дня
    day_total = {
            'amount': 0,
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbohydrate': 0,
            }
    # итоговые вес и калории по каждому виду продуктов для ТОПов
    total_by_prod = {}

    # обработка каждой записи о продукте
    for food in food_entry:

        # подсчет количеств блюд для каждой категории для таблички
        count_meal_in_category[food['meal']] += 1

        # получение инфы об этом продукте
        temp_food_cache = {}
            # сначала в кеше
        if food_cache.get(food['food_id']):
            food_info = food_cache[food['food_id']]
        else:
            # потом в FatSecret
            # добавить обработчик ошибки!
            food_info = fs.food_get(food_id=food['food_id'])
            sleep(2)

            # обработка для компактного сохранения
            if type(food_info['servings']['serving']) is dict:
                temp_food_cache[food_info['food_id']] = {
                    'food_name': food_info['food_name'],
                    'servings': {
                        'serving': {
                            'serving_id': food_info['servings']['serving']['serving_id'],
                            'measurement_description': food_info['servings']['serving']['measurement_description'],
                            'metric_serving_amount': food_info['servings']['serving'].get('metric_serving_amount', None),
                            'number_of_units': food_info['servings']['serving']['number_of_units'],
                            'metric_serving_unit': food_info['servings']['serving'].get('metric_serving_unit', None),
                            'serving_description': food_info['servings']['serving']['serving_description'] }}}
            else:
                temp_food_cache[food_info['food_id']] = {
                    'food_name': food_info['food_name'],
                    'servings': {
                        'serving': [] }}
                for dic in food_info['servings']['serving']:
                    temp_food_cache[food_info['food_id']]['servings']['serving'].append({
                        'serving_id': dic['serving_id'],
                        'measurement_description': dic['measurement_description'],
                        'metric_serving_amount': dic.get('metric_serving_amount', None),
                        'number_of_units': dic['number_of_units'],
                        'metric_serving_unit': dic.get('metric_serving_unit', None),
                        'serving_description': dic['serving_description'] })

            # сохранение в кеш
            food_cache.update(temp_food_cache)


        # добавление инфы в food для соответствующего вида порции
        if type(food_info['servings']['serving']) is list:
            for serv_info in food_info['servings']['serving']:
                if serv_info['serving_id'] == food['serving_id']:
                    food['serving'] = serv_info
                    break
        else:
            food['serving'] = food_info['servings']['serving']
        
        # добавляем номальное отображение количества
        # если измерение в г или мл - считаем как есть
        if (food['serving']['measurement_description'] == 'g' or
            food['serving']['measurement_description'] == 'ml'):
            food['norm_amount'] = int(float(food['number_of_units']))
            day_total['amount'] += food['norm_amount']
        else:
            # если измерение в порциях - сначала проверяем, есть ли граммовка порции
            if food['serving'].get('metric_serving_amount') is None:
                # если в инфе не оказалось граммовки порции
                # добавляем эту еду в спец.словарь и не считаем amount
                prods_without_info[food['food_id']] = {
                    'food_entry_name': food['food_entry_name'],
                    'serving_description': food['serving'].get('serving_description', 'порция'),
                    'serving_id': food['serving_id'],
                    'calories_per_serving': food['serving'].get('calories', food['calories']) }
            else:
                # если в инфе метрика есть - считаем и добавляем к общему подсчету
                food['norm_amount'] = int(float(food['number_of_units']) *
                                        float(food['serving']['metric_serving_amount']) *
                                        float(food['serving']['number_of_units']))
                day_total['amount'] += food['norm_amount']            

        # подсчет итоговой суммы кбжу
        day_total['calories'] += int(food['calories'])
        day_total['protein'] += float(food['protein'])
        day_total['fat'] += float(food['fat'])
        day_total['carbohydrate'] += float(food['carbohydrate'])

        # ТОПЫ
        # нормальное общее наименование еды для топов
        food['food_name'] = food_info['food_name']
        # подсчет
        if total_by_prod.get(food['food_name']) == None:
            total_by_prod[food['food_name']] = {
                'calories': 0,
                'amount': 0,
            }
        total_by_prod[food['food_name']]['calories'] += int(food['calories'])
        if food.get('norm_amount'):
            total_by_prod[food['food_name']]['amount'] += food['norm_amount']
            total_by_prod[food['food_name']]['metric'] = food['serving']['metric_serving_unit']

    # записывается измененный кеш обратно в файл
    with open('personalpage/food_cache.pickle', 'wb') as f:
        pickle.dump(food_cache, f)

    # нумерация продуктов без инфы о порции
    index_number = 1
    for prod in prods_without_info:
        prods_without_info[prod]['index_number'] = index_number
        index_number += 1

    # округляем результаты в получившемся итоге по кбжу
    for key, value in day_total.items():
        day_total[key] = round(value, 2)
           
    # сортировка ТОПов
    top_calories = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['calories'], reverse=True)[:3])
    top_amount = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['amount'], reverse=True)[:3])

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'top_calories': top_calories,
        'top_amount': top_amount,
        'total_by_prod': total_by_prod,
        'day_total': day_total,
        'count_meal_in_category': count_meal_in_category,
        'prods_without_info': prods_without_info,
        'briefdate': briefdate,
        'prev_date': prev_date,
        'next_date': next_date,
        'food_entry': food_entry,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_foodbydate.html', data)


def client_foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
       с кнопочкой подсчета ТОПов
    """
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)

    # делаем сессию с FatSecret
    make_session(client_id)

     # месяц, за который нужно посчитать стату,
     # введенный на предыдущей странице
    briefmonth = request.GET.get('month')
    if briefmonth is None or not briefmonth:
        return redirect('client_mealjournal')

    # заготовки для html
    year = int(briefmonth[0:4])
    month = int(briefmonth[-2:])

    if month == 1:
        prev_month = f"{year - 1}-12"
        next_month = f"{year}-02"
    elif month == 9:
        prev_month = f"{year}-08"
        next_month = f"{year}-10"
    elif month == 10:
        prev_month = f"{year}-09"
        next_month = f"{year}-11"
    elif month == 11:
        prev_month = f"{year}-10"
        next_month = f"{year}-12"
    elif month == 12:
        prev_month = f"{year}-11"
        next_month = f"{year + 1}-01"
    else:
        prev_month = f"{year}-0{month - 1}"
        next_month = f"{year}-0{month + 1}"

    try:
        # форматируем формат введенного месяца для FS
        briefmonth = datetime.strptime(briefmonth, "%Y-%m")
        # получаем нужные данные от FS за месяц
        food_entries_month = fs.food_entries_get_month(date=briefmonth)
        sleep(3)
    except KeyError:
        # если данных нет - переменная будет пустой
        # указать конкретный тип ошибки!
        food_entries_month = ""

    # переменные для подсчета средних значений кбжу
    avg_protein = 0
    avg_fat = 0
    avg_carbo = 0
    avg_calories = 0

    # считаем средние значения кбжу:
    if food_entries_month:
        # если за месяц одна запись - будет просто словарь
        if type(food_entries_month) is dict:
            food_entries_month['date_int'] = (date(1970, 1, 1) + 
                        timedelta(days=int(food_entries_month['date_int'])))
            avg_protein = food_entries_month['protein']
            avg_fat = food_entries_month['fat']
            avg_carbo = food_entries_month['carbohydrate']
            avg_calories = food_entries_month['calories']
            # превращаем в список из словаря, чтобы табличка не ебнулась
            food_entries_month = [food_entries_month]
        else:
            # считаем среднее арифметическое для кбжу
            days_count = len(food_entries_month)
            for day in food_entries_month:
                day['date_int'] = date(1970, 1, 1) + timedelta(days=int(day['date_int']))
                avg_protein += float(day['protein'])
                avg_fat += float(day['fat'])
                avg_carbo += float(day['carbohydrate'])
                avg_calories += float(day['calories'])
            avg_protein = round(avg_protein / days_count, 2)
            avg_fat = round(avg_fat / days_count, 2)
            avg_carbo = round(avg_carbo / days_count, 2)
            avg_calories = round(avg_calories / days_count, 2)

    # предыдущий месяц для подстановки в поле выбора
    previous_month = date.today() + relativedelta(months=-1)
    previous_month = str(previous_month)[0:7]

    # переменные для ТОПов
    top_calories = ""
    top_amount = ""
    # продукты, для которых нет инфо о граммовке порции
    prods_without_info = {}

    # создание ТОП-списков! (если нажать на кнопку)
    if request.GET.get('top_create', False):
        print('считаю топ')

        # итоговые вес и калории по каждому продукту
        total_by_prod = {}

        # открываем сохраненные данные о продуктах из файла
        with open('personalpage/food_cache.pickle', 'rb') as file:
            food_cache = pickle.load(file)

        # для каждого дня в записях за месяц
        for day in food_entries_month:
            # берем дату записи
            food_date = datetime.combine(day['date_int'], time())
            # получаем список съеденных продуктов за эту дату
            try:
                food_entry = fs.food_entries_get(date=food_date)
            except GeneralError:
                print('спим')
                sleep(30)
                print('просыпаемся')
                food_entry = fs.food_entries_get(date=food_date)
            sleep(3)

            # для каждого продукта в списке съеденного за день
            for food in food_entry:

                # получение инфы об этом продукте
                temp_food_cache = {}
                    # сначала в кеше
                if food_cache.get(food['food_id']):
                    food_info = food_cache[food['food_id']]
                else:
                    # потом в FatSecret
                    # добавить обработчик ошибки!
                    try:
                        print('запрошен реквест о еде, food_id: ' + food['food_id'])
                        food_info = fs.food_get(food_id=food['food_id'])
                    except GeneralError:
                        print('спим')
                        sleep(30)
                        print('просыпаемся')
                        food_info = fs.food_get(food_id=food['food_id'])
                    sleep(3)

                    # обработка для компактного сохранения
                    if type(food_info['servings']['serving']) is dict:
                        temp_food_cache[food_info['food_id']] = {
                            'food_name': food_info['food_name'],
                            'servings': {
                                'serving': {
                                    'serving_id': food_info['servings']['serving']['serving_id'],
                                    'measurement_description': food_info['servings']['serving']['measurement_description'],
                                    'metric_serving_amount': food_info['servings']['serving'].get('metric_serving_amount', None),
                                    'number_of_units': food_info['servings']['serving']['number_of_units'],
                                    'metric_serving_unit': food_info['servings']['serving'].get('metric_serving_unit', None),
                                    'serving_description': food_info['servings']['serving']['serving_description'] }}}
                    else:
                        temp_food_cache[food_info['food_id']] = {
                            'food_name': food_info['food_name'],
                            'servings': {
                                'serving': [] }}
                        for dic in food_info['servings']['serving']:
                            temp_food_cache[food_info['food_id']]['servings']['serving'].append({
                                'serving_id': dic['serving_id'],
                                'measurement_description': dic['measurement_description'],
                                'metric_serving_amount': dic.get('metric_serving_amount', None),
                                'number_of_units': dic['number_of_units'],
                                'metric_serving_unit': dic.get('metric_serving_unit', None),
                                'serving_description': dic['serving_description'] })

                    # сохранение в кеш
                    food_cache.update(temp_food_cache)
                        
                    
                # добавление инфы в food для соответствующего вида порции
                if type(food_info['servings']['serving']) is list:
                    for serv_info in food_info['servings']['serving']:
                        if serv_info['serving_id'] == food['serving_id']:
                            food['serving'] = serv_info
                            break
                else:
                    food['serving'] = food_info['servings']['serving']

                # добавляем нормальное отображение количества
                # если измерение в г или мл - считаем как есть
                if (food['serving']['measurement_description'] == 'g' or
                    food['serving']['measurement_description'] == 'ml'):
                    food['norm_amount'] = int(float(food['number_of_units']))
                else:
                    # если измерение в порциях - сначала проверяем, есть ли граммовка порции
                    if food['serving'].get('metric_serving_amount') is None:
                        # если в инфе не оказалось граммовки порции
                        # добавляем эту еду в спец.словарь и не считаем
                        prods_without_info[food['food_id']] = {
                            'food_entry_name': food['food_entry_name'],
                            'serving_description': food['serving'].get('serving_description', 'порция'),
                            'serving_id': food['serving_id'],
                            'calories_per_serving': food['serving'].get('calories', food['calories']) }
                    else:
                        # если в инфе метрика есть - считаем
                        food['norm_amount'] = int(float(food['number_of_units']) *
                                            float(food['serving']['metric_serving_amount']) *
                                            float(food['serving']['number_of_units']))
                                            
                # нормальное общее наименование для топов
                # ? это можно убрать - записать ниже сразу как food_info['food_name'] ?
                food['food_name'] = food_info['food_name']

                # добавление\обновление инфы об общем количестве и калориях по продукту
                # тут оптимизировать
                if food.get('norm_amount') is not None:
                    if total_by_prod.get(food['food_name']) == None:
                        total_by_prod[food['food_name']] = {
                            'calories': 0,
                            'amount': 0,
                        }
                    total_by_prod[food['food_name']]['calories'] += int(food['calories'])
                    if food.get('norm_amount'):
                        total_by_prod[food['food_name']]['amount'] += food['norm_amount']
                        total_by_prod[food['food_name']]['metric'] = food['serving']['metric_serving_unit']

        # данные посчитаны
        # можно записать обновленный кеш обратно в файл
        with open('personalpage/food_cache.pickle', 'wb') as f:
            pickle.dump(food_cache, f)
            
        # нумерация продуктов без инфы о порции
        index_number = 1
        for prod in prods_without_info:
            prods_without_info[prod]['index_number'] = index_number
            index_number += 1

        # сорировка для вывода ТОПов
        top_calories = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['calories'], reverse=True)[:10])
        top_amount = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['amount'], reverse=True)[:10])

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'top_calories': top_calories,
        'top_amount': top_amount,
        'briefmonth': briefmonth,
        'previous_month': previous_month,
        'food_entries_month': food_entries_month,
        'avg_month': {
            'calories': avg_calories,
            'protein': avg_protein,
            'fat': avg_fat,
            'carbo': avg_carbo,
        },
        'prev_month': prev_month,
        'next_month': next_month,
        'prods_without_info': prods_without_info,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_foodbymonth.html', data)


def client_anthropometry(request):
    """Антропометрические данные клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    clientname = request.GET['clientname']
    client_id = request.GET['client_id']
    client_contacts = get_client_contacts(client_id)
    # комментарий для клиента
    client_comment_form = today_commentary_form(client_id)

    # таблица сделанных измерений
    metrics = Anthropometry.objects.filter(user=client_id)
    if metrics.exists():
        if len(metrics) == 1:
            first_metrics = ''
            prev_metrics = [metrics[0]]
        elif len(metrics) == 2:
            first_metrics = metrics.earliest()
            prev_metrics = [metrics.latest()]
        else:
            first_metrics = metrics.earliest()
            prev_metrics = reversed(metrics[0:2])
    else:
        first_metrics = ''
        prev_metrics = ''

    # показ всех записей
    show_all = request.GET.get('show_all')

    # проверка текущей настройки достпуности фото
    try:
        photoaccess_instance = UserSettings.objects.get(user=client_id)
    except UserSettings.DoesNotExist:
        photoaccess_instance = UserSettings.objects.create(user_id=client_id)
        
    accessibility = photoaccess_instance.photo_access

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'first_metrics': first_metrics,
        'prev_metrics': prev_metrics,
        'metrics': metrics,
        'show_all': show_all,
        'accessibility': accessibility,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
    }
    return render(request, 'controlpage/client_anthropometry.html', data)