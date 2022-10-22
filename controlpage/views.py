import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from personalpage.models import Measurement, Questionary, FatSecretEntry
from personalpage.forms import QuestionaryForm
from time import sleep
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from personalpage.views import make_avg_for_period
from fatsecret import Fatsecret, GeneralError


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


# Create your views here.
def controlpage(request):
    """Личный кабинет Параболы"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # список зарегистрированных клиентов
    # clients = User.objects.exclude(username='Demmenty').exclude(username='Parrabolla')
    clients = User.objects.exclude(username='Parrabolla')

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
        'fs_connected': fs_connected,
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

    # делаем сессию с FatSecret
    make_session(client_id)

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

    # для поля выбора
    today_day = str(date.today())
    previous_month = str(date.today() + relativedelta(months=-1))[0:7]

    data = {
        'clientname': clientname,
        'client_id': client_id,
        'food_entries_month': food_entries_month,
        'prods_without_info': prods_without_info,
        'avg_month': avg_month,
        'food_entry': food_entry,
        'day_total': day_total,
        'count_meal_in_category': count_meal_in_category,
        'today_day': today_day,
        'previous_month': previous_month,
    }
    return render(request, 'controlpage/client_mealjournal.html', data)   