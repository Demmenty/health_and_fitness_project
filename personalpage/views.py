from django.shortcuts import render, redirect
from .models import Measurement, Questionary, FatSecretEntry, EatenProduct
from .forms import MeasurementForm, QuestionaryForm
from time import sleep
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from fatsecret import Fatsecret
import pickle

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

# оптимизировать!!
def make_weekmeasureforms(request):
    """Генерация списка формочек за неделю
       Плюс автозаполнение кбжу из FatSecret
    """
    week_measureforms = []
    tmp_cash = {}

    try:
        # берем данные для доступа к FS из БД
        userdata = FatSecretEntry.objects.get(user=request.user)
        session_token = (userdata.oauth_token, userdata.oauth_token_secret)
        fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)
        # получаем данные кбжу этого месяца со срезом - посл. 7дней
        food_data = fs.food_entries_get_month()[:-8:-1]
        fs_connected = True

    except FatSecretEntry.DoesNotExist:
        fs_connected = False
        # если FS не подключен
    
    for i in range(7):
        measure_date = date.today() - timedelta(days=i)
        try:
            # если запись за этот день есть, то формочка создается на ее основе
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)

        except Measurement.DoesNotExist:
            # если записи за этот день нет, то формочка создается пустая
            measure_form = MeasurementForm()

            # в нее сразу записывается user, дата и день недели
            measure_form = measure_form.save(commit=False)
            measure_form.user = request.user
            measure_form.date = measure_date
            measure_form.weekday = WEEKDAY_RU[measure_date.weekday()][0]
            # сохраняется запись в базе
            measure_form.save()

            # готовая форма на основе сущетсвующей пустой записи БД
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)

        if fs_connected:
            # перевод даты в формат FS
            date_int = (measure_date - date(1970, 1, 1)).days
            # записываем кбжу в форму
            measure_form = measure_form.save(commit=False)
            # запись кбжу из FS для каждого дня
            # сортировать сначала по дате ?? (key=lambda x: x['date_int'])
            for day in food_data:
                if day['date_int'] == str(date_int):
                    # проверка на то, поменялись ли калории 
                    if measure_form.calories != int(day['calories']):
                        calories_changed = True
                        measure_form.calories = int(day['calories'])
                        measure_form.protein = float(day['protein'])
                        measure_form.fats = float(day['fat'])
                        measure_form.carbohydrates = float(day['carbohydrate'])
                        break

            total_by_prod = {}
            # сохраняем данные о съеденных продуктах
            # список съеденных продуктов за выбранную дату
            sleep(5)
            food_entry = fs.food_entries_get(date=datetime.combine(measure_date, time()))
            # для каждого продукта
            for food in food_entry:
                # получение инфы об этом продукте из FS
                # попробовать оптимизировать так:
                # food_info = tmp_cash.setdefault(food['food_id'], fs.food_get(food_id=food['food_id']))
                sleep(5)
                food_info = fs.food_get(food_id=food['food_id'])
                
                # получение инфы о соотв.виде порции
                if type(food_info['servings']['serving']) is list:
                    for i in food_info['servings']['serving']:
                        if i['serving_id'] == food['serving_id']:
                            food['serving'] = i
                else:
                    food['serving'] = food_info['servings']['serving']
                    
                # добавляем номальное отображение количества
                if (food['serving']['measurement_description'] == 'g' or
                    food['serving']['measurement_description'] == 'ml'):
                    food['norm_amount'] = int(float(food['number_of_units']))
                else:
                    food['norm_amount'] = int(float(food['number_of_units']) *
                                            float(food['serving']['metric_serving_amount']) *
                                            float(food['serving']['number_of_units']))
                # если одноименного продукта не записано уже, создается новая строчка
                if total_by_prod.get(food['food_entry_name']) == None:
                    total_by_prod[food['food_entry_name']] = {
                        'calories': 0,
                        'amount': 0,
                        }
                total_by_prod[food['food_entry_name']]['calories'] += int(food['calories'])
                total_by_prod[food['food_entry_name']]['amount'] += food['norm_amount']
                total_by_prod[food['food_entry_name']]['metric'] = food['serving']['metric_serving_unit']

        # запись данных о съеденной еде в бд
        if total_by_prod:
            # удалить сущетсвовавшие записи за этот день
            # так так они могли измениться
            # или прописать какое-то условие, калории поменялись напр
            if True:
                EatenProduct.objects.filter(day=measure).delete()
                
            for product in total_by_prod.items():
                entry = EatenProduct(product_name=product[0],
                                    product_amount=product[1]['amount'],
                                    product_metric=product[1]['metric'],
                                    product_calories=product[1]['calories'],
                                    day=measure)
                entry.save()


        # это здесь точно нужно?
        # measure_form.save()

        # # если это удалить - не работает
        # measure = Measurement.objects.get(date=measure_date, user=request.user)
        # measure_form = MeasurementForm(instance=measure)
        # добавление формы в список форм недели


        week_measureforms.append(measure_form)

    return week_measureforms


def make_avg_for_period(user, period=7):
    """Составляет словарь из средних значений по
       каждому измерению за неделю.
       Нужно передать user и period = кол-во дней
    """
    set = reversed(Measurement.objects.filter(user=user)[:period])
    avg_data = {
        'avg_feel': 0,
        'avg_weight': 0,
        'avg_fat': 0,
        'avg_pulse': 0,
        'avg_pressure': 0,
        'avg_calories': 0,
        'avg_protein': 0,
        'avg_fats': 0,
        'avg_carbohydrates': 0,
    }
    pressure_upper = 0
    pressure_lower = 0

    count_feel = 0
    count_weight = 0
    count_fat = 0
    count_pulse = 0
    count_pressure = 0
    count_calories = 0
    count_protein = 0
    count_fats = 0
    count_carbohydrates = 0

    for day in set:
        if day.feel:
            avg_data['avg_feel'] += int(day.feel)
            count_feel += 1
        if day.weight:
            avg_data['avg_weight'] += float(day.weight)
            count_weight += 1
        if day.fat:
            avg_data['avg_fat'] += float(day.fat)
            count_fat += 1
        if day.pulse:
            avg_data['avg_pulse'] += int(day.pulse)
            count_pulse += 1
        if day.pressure_upper and day.pressure_lower:
            pressure_upper += int(day.pressure_upper)
            pressure_lower += int(day.pressure_lower)
            count_pressure += 1
        # кбжу - без учета сегодняшнего дня
        if day.calories and day.date != date.today():
            avg_data['avg_calories'] += int(day.calories)
            count_calories += 1
        if day.protein and day.date != date.today():
            avg_data['avg_protein'] += float(day.protein)
            count_protein += 1
        if day.fats and day.date != date.today():
            avg_data['avg_fats'] += float(day.fats)
            count_fats += 1
        if day.carbohydrates and day.date != date.today():
            avg_data['avg_carbohydrates'] += float(day.carbohydrates)
            count_carbohydrates += 1

    if count_feel:
        avg_data['avg_feel'] = round(avg_data['avg_feel'] / count_feel, 1)
    if count_weight:
        avg_data['avg_weight'] = round(avg_data['avg_weight'] / count_weight, 1)
    if count_fat:
        avg_data['avg_fat'] = round(avg_data['avg_fat'] / count_fat, 1)
    if count_pulse:
        avg_data['avg_pulse'] = int(avg_data['avg_pulse'] / count_pulse)
    if count_pressure:
        avg_data['avg_pressure'] = str(int(pressure_upper / count_pressure)) + "/" + str(int(pressure_lower / count_pressure))
    if count_calories:
        avg_data['avg_calories'] = int(avg_data['avg_calories'] / count_calories)
    if count_protein:
        avg_data['avg_protein'] = int(avg_data['avg_protein'] / count_protein)
    if count_fats:
        avg_data['avg_fats'] = int(avg_data['avg_fats'] / count_fats)
    if count_carbohydrates:
        avg_data['avg_carbohydrates'] = int(avg_data['avg_carbohydrates'] / count_carbohydrates)
    
    return avg_data


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


# данные fatsecret
consumer_key = '96509fd6591d4fb384386e1b75516777'
consumer_secret = 'cb1398ad47344691b092cabce5647116'
fs = Fatsecret(consumer_key, consumer_secret)

def make_session(user):
    # берем данные для доступа из БД
    global fs
    userdata = FatSecretEntry.objects.get(user=user)
    session_token = (userdata.oauth_token, userdata.oauth_token_secret)
    fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)


# My views
def personalpage(request):
    """Личный кабинет клиента"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # Парабола перенаправляется на свою страницу
    if request.user.username == 'Parrabolla':
        return redirect('controlpage')

    # существоавние анкеты
    try:
        questionary_existing = Questionary.objects.get(user=request.user)
    except Questionary.DoesNotExist:
        questionary_existing = ''

    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
        try:
            # берем данные для доступа к FS из БД
            userdata = FatSecretEntry.objects.get(user=request.user)
            session_token = (userdata.oauth_token, userdata.oauth_token_secret)
            fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)
            # получаем данные кбжу этого месяца - последняя запись
            food_data = fs.food_entries_get_month()[-1]
            # сегодняшняя дата в формате FS
            today_date_int = str((date.today() - date(1970, 1, 1)).days)
            # если посл.запись - сегодня, то записываем ее данные
            if food_data['date_int'] == today_date_int:
                today_measure.calories = food_data['calories']
                today_measure.protein = food_data['protein']
                today_measure.fats = food_data['fat']
                today_measure.carbohydrates = food_data['carbohydrate']
                today_measure.save()

        except FatSecretEntry.DoesNotExist:
            ...
            # если FS не подключен

    else:
        today_measure = ''

    # список данных измерений за неделю
    week = reversed(Measurement.objects.filter(user=request.user)[:7])
    # средние значения измерений за неделю 
    avg_week = make_avg_for_period(request.user, period=7)

    # статистика за выбранный период
    if request.GET.get('selectperiod'):
        selected_period = int(request.GET.get('selectperiod'))
        # средние значения измерений за произвольный период
        avg_period = make_avg_for_period(request.user, period=selected_period)
        # список измерений за этот период
        period = reversed(Measurement.objects.filter(user=request.user)[:selected_period])
        # красивый формат
        selected_period = str(selected_period) + " " + get_noun_ending(selected_period, 'день', 'дня', 'дней')
    
    else:
        selected_period = ""
        avg_period = ""
        period = ""

    data = {
        'today_measure': today_measure,
        'week': week,
        'selected_period': selected_period,
        'period': period,
        'avg_week': avg_week,
        'avg_period': avg_period,
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
            total_by_prod = {}
            # проверка, что FS подключен
            try:
                make_session(request.user)

                # отправляем вес в FatSecret
                # получаем вес из формы
                measure_weight = form.cleaned_data['weight']
                # если вес вообще записан
                if measure_weight:
                    # проверка что дата измерения не старше 2 дней назад иначе FS не примет
                    if (date.today() - measure_date).days >= -2:
                        # получение даты последнего веса из FS (из профиля неверная)
                        last_weight_date_int = fs.weights_get_month()[-1]['date_int']
                        # переводим в нормальную дату
                        last_weight_date = date(1970, 1 ,1) + timedelta(days=int(last_weight_date_int))
                        # если дата последне записанного в FS веса старее, чем текущая дата
                        if last_weight_date < measure_date:
                            # записываем вес в FS (нельзя чтобы перезаписывалось)
                            fs.weight_update(current_weight_kg=float(measure_weight), date=datetime.combine(measure_date, time()))
                

                

            except FatSecretEntry.DoesNotExist:
                ...
            # сохранение формы
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


# # для очистки файла кеша - раскомментировать
# with open('personalpage/food_cache.pickle', 'wb') as f:
#     pickle.dump({}, f)



def mealjournal(request):
    """Страница контроля питания и кбжу"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # GET-запрос
    if request.method == 'GET':

        # продукты, для которых нет инфо о граммовке порции
        prods_without_info = {}

        with open('personalpage/food_cache.pickle', 'rb') as file:
            food_cache = pickle.load(file)

        try:
            # делаем сессию с FS для user
            make_session(request.user)

            # данные для тех, у кого подключен FatSecret

            # питание за сегодняшний день
            food_entry = fs.food_entries_get(date=datetime.today())
            # питание за текущий месяц
            food_entries_month = fs.food_entries_get_month(date=datetime.today())


            # данные для сегодня
            # категории
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
            
            # каждая запись о продукте
            for food in food_entry:

                temp_food_cache = {}

                count_meal_in_category[food['meal']] += 1

                print('новый круг цикла. food in food_entry:')
                print(food)
                print()

                day_total['calories'] += int(food['calories'])
                day_total['protein'] += float(food['protein'])
                day_total['fat'] += float(food['fat'])
                day_total['carbohydrate'] += float(food['carbohydrate'])


                # получение инфы об этом продукте
                if food_cache.get(food['food_id']):
                    print('инфо найдена в кеше, вот она, food_info:')
                    food_info = food_cache[food['food_id']]
                    print(food_info)
                    print()
                else:
                    # добавить обработчик ошибки! (с таймером - если много запросов)
                    print('запрошен реквест о еде, food_id: ' + food['food_id'])
                    food_info = fs.food_get(food_id=food['food_id'])
                    print('вот сырой food_info:')
                    print(food_info)
                    print()
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

                    if type(food_info['servings']['serving']) is list:
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

                    print('Обработанный кеш, temp_food_cache:')
                    print(temp_food_cache)
                    print()                    

                    # сохранение в кеш
                    food_cache.update(temp_food_cache)


                # получение инфы о соотв.виде порции
                if type(food_info['servings']['serving']) is list:
                    for i in food_info['servings']['serving']:
                        if i['serving_id'] == food['serving_id']:
                            food['serving'] = i
                else:
                    food['serving'] = food_info['servings']['serving']
                

                print('что записано в food после обработки, перед обработкой количества')
                print(food)
                print()

                # добавляем нормальное отображение количества
                # если измерение в г или мл - считаем как есть
                if (food['serving']['measurement_description'] == 'g' or
                    food['serving']['measurement_description'] == 'ml'):
                    food['norm_amount'] = int(float(food['number_of_units']))
                    day_total['amount'] += food['norm_amount']
                else:
                    # если измерение в порциях - сначала проверяем, есть ли граммовка порции
                    if food['serving'].get('metric_serving_amount') is None:
                        print('метрики в food не оказалось')
                        print()
                        # если в инфе не оказалось граммовки порции
                        # добавляем эту еду в спец.словарь и не считаем
                        prods_without_info[food['food_id']] = {
                            'food_entry_name': food['food_entry_name'],
                            'serving_description': food['serving'].get('serving_description', 'порция'),
                            'serving_id': food['serving_id'] }
                        print('так выглядит prods_without_info')
                        print(prods_without_info)
                        print()
                    else:
                        # если в инфе метрика есть - считаем и добавляем к общему подсчету
                        print('метрика есть')
                        print()
                        food['norm_amount'] = int(float(food['number_of_units']) *
                                            float(food['serving']['metric_serving_amount']) *
                                            float(food['serving']['number_of_units']))
                        day_total['amount'] += food['norm_amount']

                        print('круг цикла пройден')
                        print()
                        print()

            for key, value in day_total.items():
                day_total[key] = round(value, 2)

            with open('personalpage/food_cache.pickle', 'wb') as f:
                pickle.dump(food_cache, f)

            # подсчет средних значений за месяц
            # если за день нет записей - то она итак не отображается
            # поэтому тут другая формула
            avg_protein = 0
            avg_fat = 0
            avg_carbo = 0
            avg_calories = 0
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

            # предыдущий месяц для поля выбора
            previous_month = date.today() + relativedelta(months=-1)
            previous_month = str(previous_month)[0:7]

            data = {
                'food_entries_month': food_entries_month,
                'prods_without_info': prods_without_info,
                'avg_protein': avg_protein,
                'avg_fat': avg_fat,
                'avg_carbo': avg_carbo,
                'avg_calories': avg_calories,
                'food_entry': food_entry,
                'day_total': day_total,
                'count_meal_in_category': count_meal_in_category,
                'previous_month': previous_month,
                'user_not_connected': False,
            }
            return render(request, 'personalpage/mealjournal.html', data)

        except FatSecretEntry.DoesNotExist:
            # данные для тех, у кого НЕ подключен FatSecret
            data = {
                'user_not_connected': True,
            }
            return render(request, 'personalpage/mealjournal.html', data)

    # POST-запрос
    if request.method == 'POST':
        # предусмотреть вариант, когда продуктов несколько!
        # пока такой один - id '4652615'
        food_id = request.POST["food_id"]
        metric_serving_amount = request.POST["metric_serving_amount"]
        metric_serving_unit = request.POST["metric_serving_unit"]
        serving_id = request.POST["serving_id"]

        with open('personalpage/food_cache.pickle', 'rb') as file:
            food_cache = pickle.load(file)

        if type(food_cache[food_id]['servings']['serving']) is dict:
            food_cache[food_id]['servings']['serving']["metric_serving_amount"] = metric_serving_amount
            food_cache[food_id]['servings']['serving']["metric_serving_unit"] = metric_serving_unit
        else:
            for dic in food_cache[food_id]['servings']['serving']:
                if dic['serving_id'] == serving_id:
                    dic["metric_serving_amount"] = metric_serving_amount
                    dic["metric_serving_unit"] = metric_serving_unit
                    break

        with open('personalpage/food_cache.pickle', 'wb') as f:
                pickle.dump(food_cache, f)
        
        return redirect('mealjournal')



def foodbydate(request):
    """Получение данных за опр.день из FatSecret"""
    # делаем сессию с FS для user
    make_session(request.user)

    # получаем введенную дату
    briefdate = request.GET['date']
    # форматируем
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")
    # получаем нужные данные от FS

    # категории
    count_meal_in_category = {
        'Breakfast': 0,
        'Lunch': 0,
        'Dinner': 0,
        'Other': 0,
    }
    # итоговые вес и калории по продуктам
    total_by_prod = {}
    # итоговые кбжу дня
    day_total = {
            'amount': 0,
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbohydrate': 0,
            }
    
    # список съеденных продуктов за выбранную дату
    food_entry = fs.food_entries_get(date=briefdate)
    # каждая запись о продукте
    for food in food_entry:
        # получение инфы об этом продукте
        food_info = fs.food_get(food_id=food['food_id'])
        # получение инфы о соотв.виде порции
        if type(food_info['servings']['serving']) is list:
            for i in food_info['servings']['serving']:
                if i['serving_id'] == food['serving_id']:
                    food['serving'] = i
        else:
            food['serving'] = food_info['servings']['serving']
        
        # добавляем номальное отображение количества
        if (food['serving']['measurement_description'] == 'g' or
            food['serving']['measurement_description'] == 'ml'):
            food['norm_amount'] = int(float(food['number_of_units']))
        else:
            food['norm_amount'] = int(float(food['number_of_units']) *
                                  float(food['serving']['metric_serving_amount']) *
                                  float(food['serving']['number_of_units']))
        
        if food['meal'] == 'Breakfast':
            count_meal_in_category['Breakfast'] += 1
        if food['meal'] == 'Lunch':
            count_meal_in_category['Lunch'] += 1
        if food['meal'] == 'Dinner':
            count_meal_in_category['Dinner'] += 1
        if food['meal'] == 'Other':
            count_meal_in_category['Other'] += 1

        # нормальное общее наименование для топов
        food['food_name'] = food_info['food_name']

        if total_by_prod.get(food['food_name']) == None:
            total_by_prod[food['food_name']] = {
                'calories': 0,
                'amount': 0,
            }

        total_by_prod[food['food_name']]['calories'] += int(food['calories'])
        total_by_prod[food['food_name']]['amount'] += food['norm_amount']
        total_by_prod[food['food_name']]['metric'] = food['serving']['metric_serving_unit']

        day_total['amount'] += food['norm_amount']
        day_total['calories'] += int(food['calories'])
        day_total['protein'] += float(food['protein'])
        day_total['fat'] += float(food['fat'])
        day_total['carbohydrate'] += float(food['carbohydrate'])

    for key, value in day_total.items():
        day_total[key] = round(value, 2)

    top_calories = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['calories'], reverse=True)[:3])
    top_amount = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['amount'], reverse=True)[:3])

    data = {
        'top_calories': top_calories,
        'top_amount': top_amount,
        'total_by_prod': total_by_prod,
        'day_total': day_total,
        'count_meal_in_category': count_meal_in_category,
        'briefdate': briefdate,
        'food_entry': food_entry,
    }
    return render(request, 'personalpage/foodbydate.html', data)


def foodbymonth(request):
    """Получение данных за опр.месяц из FatSecret"""
    # делаем сессию с FS для user
    make_session(request.user)

    briefmonth = request.GET['month']
    # форматируем
    
    briefmonth = datetime.strptime(briefmonth, "%Y-%m")



    food_info = fs.food_get(food_id='4652615')
    print('сырой:')
    print(food_info)
    print()



    try:
        # получаем нужные данные от FS за месяц
        food_entries_month = fs.food_entries_get_month(date=briefmonth)
    except KeyError:
        food_entries_month = ""

    # считаем средние значения
    avg_protein = 0
    avg_fat = 0
    avg_carbo = 0
    avg_calories = 0


    if food_entries_month:

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

    # предыдущий месяц для поля выбора
    previous_month = date.today() + relativedelta(months=-1)
    previous_month = str(previous_month)[0:7]

    top_calories = ""
    top_amount = ""

    # создание ТОП-списков!
    if request.GET.get('top_create', False):

        # итоговые вес и калории по продуктам
        total_by_prod = {}

        # продукты, для которых нет инфо о граммовке порции
        prods_without_info = {}
        
        with open('personalpage/food_cache.pickle', 'rb') as file:
            food_cache = pickle.load(file)
            print('ЭТО food_cache')
            print(food_cache)
            print()

        # для каждого дня в записях за месяц
        for day in food_entries_month:
            food_date = datetime.combine(day['date_int'], time())
            
            # список съеденных продуктов за выбранную дату
            food_entry = fs.food_entries_get(date=food_date)
            sleep(5)

            # для каждого продукта в записи о съеденном за день
            for food in food_entry:

                temp_food_cache = {}
                # получение инфы об этом продукте
                if food_cache.get(food['food_id']):
                    print('инфо найдена в кеше')
                    food_info = food_cache[food['food_id']]
                    print()
                else:
                    # добавить обработчик ошибки!
                    print('запрошен реквест о еде, food_id: ' + food['food_id'])
                    food_info = fs.food_get(food_id=food['food_id'])
                    print('сырой:')
                    print(food_info)
                    sleep(5)


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
                                    'metric_serving_unit': food_info['servings']['serving'].get('metric_serving_unit', None) }}}
                        # если в инфе не оказалось граммовки порции
                        if temp_food_cache[food_info['food_id']]['servings']['serving']['metric_serving_amount'] is None:
                            prods_without_info[[food_info['food_id']]] = {
                                'food_name': food_info['food_name'],
                                'serving_description': food_info['servings']['serving'].get('serving_description', 'порция'),
                                'brand_name': food_info['brand_name']  }
                            continue

                    if type(food_info['servings']['serving']) is list:
                        temp_food_cache[food_info['food_id']] = {
                            'food_name': food_info['food_name'],
                            'servings': {
                                'serving': [] }}
                        
                        for dic in food_info['servings']['serving']:
                            temp_food_cache[food_info['food_id']]['servings']['serving'].append({
                                'serving_id': dic['serving_id'],
                                'measurement_description': dic['measurement_description'],
                                'metric_serving_amount': dic['metric_serving_amount'],
                                'number_of_units': dic['number_of_units'],
                                'metric_serving_unit': dic['metric_serving_unit'] })

                    print('Обработанный кеш')
                    print(temp_food_cache)
                    print()

                    # сохранение в кеш
                    food_cache.update(temp_food_cache)
                    
                
                # получение инфы о соотв.виде порции
                if type(food_info['servings']['serving']) is list:
                    for i in food_info['servings']['serving']:
                        if i['serving_id'] == food['serving_id']:
                            food['serving'] = i
                else:
                    food['serving'] = food_info['servings']['serving']

                # добавляем нормальное отображение количества
                if (food['serving']['measurement_description'] == 'g' or
                    food['serving']['measurement_description'] == 'ml'):
                    food['norm_amount'] = int(float(food['number_of_units']))
                else:
                    food['norm_amount'] = int(float(food['number_of_units']) *
                                        float(food['serving']['metric_serving_amount']) *
                                        float(food['serving']['number_of_units']))
                                        
                # нормальное общее наименование для топов
                food['food_name'] = food_info['food_name']

                if total_by_prod.get(food['food_name']) == None:
                    total_by_prod[food['food_name']] = {
                        'calories': 0,
                        'amount': 0,
                    }

                total_by_prod[food['food_name']]['calories'] += int(food['calories'])
                total_by_prod[food['food_name']]['amount'] += food['norm_amount']
                total_by_prod[food['food_name']]['metric'] = food['serving']['metric_serving_unit']


        with open('personalpage/food_cache.pickle', 'wb') as f:
            pickle.dump(food_cache, f)
        

        top_calories = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['calories'], reverse=True)[:5])
        top_amount = dict(sorted(total_by_prod.items(), key=lambda x: x[1]['amount'], reverse=True)[:5])


    data = {
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
        'prods_without_info': prods_without_info,
    }
    return render(request, 'personalpage/foodbymonth.html', data)


def fatsecretauth(request):
    """Подключение к FatSecret"""

    if request.GET.get('oauth_verifier', None):
        # получаем данные от response FatSecret
        verifier_pin = request.GET.get('oauth_verifier')
        # аутентифицирование сеанса и получение токена доступа
        session_token = fs.authenticate(verifier_pin)
        # записываем данные для сессии в базу
        FatSecretEntry.objects.create(user=request.user, oauth_token=session_token[0], oauth_token_secret=session_token[1])
        return redirect('mealjournal')

    else:
        # получаем адрес подключения и направляем по нему
        auth_url = fs.get_authorize_url(callback_url="http://127.0.0.1:8000/personalpage/fatsecretauth/")
        # получаем oauth_token и oauth_verifier
        return redirect(auth_url)