import pickle
from django.shortcuts import render, redirect
from .models import Anthropometry, Measurement, MeasureColorField, Questionary, FatSecretEntry, UserSettings
from controlpage.models import Commentary
from django.db.models import Q
from .forms import AnthropometryForm, MeasurementForm, MeasurementCommentForm, QuestionaryForm, PhotoAccessForm, ContactsForm
from time import sleep
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from fatsecret import Fatsecret, GeneralError
from django.http import JsonResponse


# данные fatsecret - засунуть в бд!!!
consumer_key = '96509fd6591d4fb384386e1b75516777'
consumer_secret = 'cb1398ad47344691b092cabce5647116'
fs = Fatsecret(consumer_key, consumer_secret)


# # для очистки файла кеша - раскомментировать
# with open('personalpage/food_cache.pickle', 'wb') as f:
#     pickle.dump({}, f)

# id '4652615' (184г) - твистер,  id '62258251' (135г) - картоха
# удаление записей о продуктах без метрики для тестов - раскомментить

# with open('personalpage/food_cache.pickle', 'rb') as f:
#     food_cache = pickle.load(f)
#     del food_cache['4652615']
#     del food_cache['62258251']
# with open('personalpage/food_cache.pickle', 'wb') as f:
#     pickle.dump(food_cache, f)


def make_session(user):
    """создание сессии с FatSecret Api для переданного пользователя"""
    global fs
    userdata = FatSecretEntry.objects.get(user=user)
    session_token = (userdata.oauth_token, userdata.oauth_token_secret)
    fs = Fatsecret(consumer_key, consumer_secret, session_token=session_token)


def make_avg_for_period(user_id, period=7):
    """Составляет словарь из средних значений по
       каждому ежедневному измерению за неделю.
       Нужно передать user и period = кол-во дней
    """
    set = reversed(Measurement.objects.filter(user=user_id)[:period])
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


def get_expert_commentary(request):
    """Получение формы коммента клиенту для клиента
       для выбранной на странице даты через скрипт в layout"""

    if request.user.is_anonymous:
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.user.id
    comment_date = request.GET['date']

    print(request)
    print(comment_date)

    try:
        instance = Commentary.objects.get(client=client_id, date=comment_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
            'general_read': instance.general_read,
            'measurements_read': instance.measurements_read,
            'nutrition_read': instance.nutrition_read,
            'workout_read': instance.workout_read,
        }
    except Commentary.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        'general_read': True,
        'measurements_read': True,
        'nutrition_read': True,
        'workout_read': True,
        }

    return JsonResponse(data, status=200)


def mark_comment_readed(request):
    """Запись инфо о том, что коммент прочитан
       через скрипт в layout"""

    if request.user.is_anonymous:
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.user.id
    comment_date = request.GET['date']
    labelname = request.GET['label']

    # сюда не попадут запросы о несуществующих
    # из-за фильтра в javascript - controlLabelReaded()
    commentary = Commentary.objects.get(client=client_id, date=comment_date)

    if labelname == 'general':
        commentary.general_read = True
    elif labelname == 'measurements':
        commentary.measurements_read = True
    elif labelname == 'nutrition':
        commentary.nutrition_read = True
    elif labelname == 'workout':
        commentary.workout_read = True
    
    commentary.save()

    data = {}

    return JsonResponse(data, status=200)


def get_count_unread(request):
    """ получение количества непрочитаных комментов 
    через скрипт в layout"""

    if request.user.is_anonymous:
        data = {}
        return JsonResponse(data, status=403)

    unread_comments = Commentary.objects.filter(
        Q(client=request.user), 
        Q(general_read=0) | Q(measurements_read=0) | Q(nutrition_read=0) | Q(workout_read=0) 
    )
    count_of_unread = unread_comments.count()

    data = {
        'count_of_unread': count_of_unread,
    }
    return JsonResponse(data, status=200)

    


# My views

def personalpage(request):
    """Личный кабинет клиента"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')
    # Парабола перенаправляется на свою страницу
    if request.user.username == 'Parrabolla':
        return redirect('controlpage')

    # существоВание анкеты
    try:
        questionary = Questionary.objects.get(user=request.user)
    except Questionary.DoesNotExist:
        questionary = ''

    # сообщение об ошибке в контактах
    contacts_error = ''
    # cохранение контактов клиента из формы
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            try:
                instance = UserSettings.objects.get(user=request.user)
                form = ContactsForm(request.POST, instance=instance)
                form.save()
                return redirect('personalpage')
            except UserSettings.DoesNotExist:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect('personalpage')
        else:
            contacts_error = 'Контакты введены некорректно. Попробуйте ещё раз.'

    # форма контактов клиента
    contacts_filled = False
    try:
        instance = UserSettings.objects.get(user=request.user)
        contacts_form = ContactsForm(instance=instance)

        # проверка на заполненность хотя бы 1 поля
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
                contacts_filled = True
                break

    except UserSettings.DoesNotExist:
        contacts_form = ContactsForm()
        
    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
        try:
            # сверяем\записываем данные кбжу из FS
            make_session(request.user)
            try:
                # получаем из FS последнюю запись за текущий месяц
                food_data = fs.food_entries_get_month()[-1]
                # если посл.запись - сегодня, то записываем ее данные
                if food_data['date_int'] == str((date.today() - date(1970, 1, 1)).days):
                    today_measure.calories = food_data['calories']
                    today_measure.protein = food_data['protein']
                    today_measure.fats = food_data['fat']
                    today_measure.carbohydrates = food_data['carbohydrate']
                    today_measure.save()
                # если нет - то будет "нет данных"
        
            except KeyError:
                ...
                # если keyerror значит данных о еде за месяц нет

        except FatSecretEntry.DoesNotExist:
            ...
            # если FS не подключен
    else:
        today_measure = ''

    date_today = date.today()

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    data = {
        'today_measure': today_measure,
        'questionary': questionary,
        'contacts_form': contacts_form,
        'contacts_error': contacts_error,
        'contacts_filled': contacts_filled,
        'today_commentary': today_commentary,
        'date_today': date_today,
    }
    return render(request, 'personalpage/personalpage.html', data)



def measurements(request):
    """Страница отслеживания ежедневных измерений"""
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # Парабола перенаправляется на свою страницу
    if request.user.username == 'Parrabolla':
        return redirect('controlpage') 

    #измерения за сегодня
    today_set = Measurement.objects.filter(date__exact=date.today(), user=request.user)
    if today_set:
        today_measure = today_set[0]
        try:
            # сверяем\записываем данные кбжу из FS
            make_session(request.user)
            try:
                # получаем из FS последнюю запись за текущий месяц
                food_data = fs.food_entries_get_month()[-1]
                # если посл.запись - сегодня, то записываем ее данные
                if food_data['date_int'] == str((date.today() - date(1970, 1, 1)).days):
                    today_measure.calories = food_data['calories']
                    today_measure.protein = food_data['protein']
                    today_measure.fats = food_data['fat']
                    today_measure.carbohydrates = food_data['carbohydrate']
                    today_measure.save()
                # если нет - то будет "нет данных"
        
            except KeyError:
                ...
                # если keyerror значит данных о еде за месяц нет

        except FatSecretEntry.DoesNotExist:
            ...
            # если FS не подключен
    else:
        today_measure = ''

    # список измерений за неделю
    week = Measurement.objects.filter(user=request.user)[:7]
    # средние значения измерений за неделю 
    avg_week = make_avg_for_period(request.user.id, period=7)
    # измерялось ли давление (отображать или нет)
    show_pressure = False
    if any(day.pressure_upper for day in week):
        show_pressure = True

    # список форм для комментов за неделю
    week_comments_forms = []
    for day in reversed(week):
        comment_form = MeasurementCommentForm(instance=day)
        week_comments_forms.append(comment_form)

    # статистика за выбранный период
    show_pressure_period = False
    period_comments_forms = []
    if request.GET.get('selectperiod'):
        selected_period = int(request.GET.get('selectperiod'))
        # средние значения измерений за произвольный период
        avg_period = make_avg_for_period(request.user, period=selected_period)
        # список измерений за этот период
        period = Measurement.objects.filter(user=request.user)[:selected_period]
        # измерялось ли давление (отображать или нет)
        if any(day.pressure_upper for day in period):
            show_pressure_period = True
        # красивый формат
        selected_period = (str(selected_period) + " " +
                           get_noun_ending(selected_period, 'день', 'дня', 'дней'))
        # список форм для комментов
        for day in reversed(period):
            comment_form = MeasurementCommentForm(instance=day)
            period_comments_forms.append(comment_form)

    else:
        selected_period = ""
        avg_period = ""
        period = ""

    # наличие цветовых настроек для клиента
    colorset_exist = bool(MeasureColorField.objects.filter(user_id=request.user))

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    data = {
        'today_measure': today_measure,
        'week': week,
        'show_pressure': show_pressure,
        'week_comments_forms': week_comments_forms,
        'period_comments_forms': period_comments_forms,
        'selected_period': selected_period,
        'show_pressure_period': show_pressure_period,
        'period': period,
        'avg_week': avg_week,
        'avg_period': avg_period,
        'colorset_exist': colorset_exist,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/measurements.html', data)    


def commentsave(request):
    """Сохранение коммента через ajax"""
    # получаем форму из запроса
    form = MeasurementCommentForm(request.POST)
    # проверяем на корректность
    if form.is_valid():
        # получаем дату из формы
        comment_date = form.cleaned_data['date']
        # получаем запись из БД с этим числом
        measure = Measurement.objects.get(date=comment_date, user=request.user) 
        # перезаписываем
        form = MeasurementCommentForm(request.POST, instance=measure)
        form.save()
        new_comment = form.cleaned_data['comment']
        data = {
            'new_comment': new_comment,
        }
        return JsonResponse(data, status=200)


def foodmetricsave(request):
    """Сохранение введенной метрики еды через ajax"""

    status = "инфа сохранена, круто!"
    saved_food_id = []

    with open('personalpage/food_cache.pickle', 'rb') as file:
        food_cache = pickle.load(file)

    index_number = 0
    while True:
        index_number += 1
        if request.POST.get("metric_serving_amount_"+str(index_number)) is None :
            break

        elif (request.POST.get("metric_serving_amount_"+str(index_number)) == "" or 
              request.POST.get("metric_serving_amount_"+str(index_number)) == "0") :
            status = "поле оставлено пустым, алло!"
        
        else:
            food_id = request.POST["food_id_"+str(index_number)]
            saved_food_id.append("food_id_"+str(index_number))
            metric_serving_amount = request.POST["metric_serving_amount_"+str(index_number)]
            metric_serving_unit = request.POST["metric_serving_unit_"+str(index_number)]
            serving_id = request.POST["serving_id_"+str(index_number)]

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

    data = {
        'status': status,
        'saved_food_id': saved_food_id,
    }
    return JsonResponse(data, status=200)


def questionary(request):
    """Страница заполнения личной анкеты"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    # GET-запрос
    if request.method == 'GET':
        # проверяем, есть ли у клиента уже анкета
        try:
            questionary = Questionary.objects.get(user=request.user)
            # создаем форму на ее основе
            form = QuestionaryForm(instance=questionary)
        except Questionary.DoesNotExist:
            questionary = ""
             # или создаем пустую форму
            form = QuestionaryForm()

        # рендерим страницу с формой
        data = {
            'questionary': questionary,
            'form': form,
            'error': '',
            'today_commentary': today_commentary,
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
                questionary = Questionary.objects.get(user=request.user)
                form = QuestionaryForm(request.POST, instance=questionary)
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
                questionary = Questionary.objects.get(user=request.user)
                # создаем форму на ее основе
                form = QuestionaryForm(instance=questionary)
            except Questionary.DoesNotExist:
                questionary = ""
                # или создаем пустую форму
                form = QuestionaryForm()
            data = {
                'questionary': questionary,
                'form': form,
                'today_commentary': today_commentary,
                'error': 'Данные введены некорректно. Попробуйте ещё раз.',
            }
            return render(request, 'personalpage/questionary.html', data)


def addmeasure(request):
    """Страница внесения и редактирования измерений"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # ГЕНЕРАЦИЯ ФОРМ на 7 дней
    week_measureforms = []
    # получаем общие данные кбжу из FS за посл. 7дней в food_data
    food_data = []
    try:
        make_session(request.user)
        fatsecret_status = "FatSecret подключен"
        fs_connected = True
        try:
            cur_month_data = fs.food_entries_get_month()
            if type(cur_month_data) is dict:
                food_data += [cur_month_data]
            else:
                food_data += cur_month_data
            # записи за текущий месяц есть
            if date.today().day < 7:
                prev_month = datetime.today() - timedelta(weeks=4)
                try:
                    prev_month_data = fs.food_entries_get_month(date=prev_month)
                    if type(prev_month_data) is dict:
                        food_data += [prev_month_data]
                    else:
                        food_data += prev_month_data
                except KeyError:
                    # записей за прошлый месяц нет
                    ...
        except KeyError:
            # записей за текущий месяц нет
            if date.today().day < 7:
                try:
                    prev_month = datetime.today() - timedelta(weeks=4)
                    prev_month_data = fs.food_entries_get_month(date=prev_month)
                    if type(prev_month_data) is dict:
                        food_data += [prev_month_data]
                    else:
                        food_data += prev_month_data
                    # записи за прошлый месяц есть
                except KeyError:
                    # записей за прошлый месяц тоже нет - ну и в рот оно ебись
                    ...
    except FatSecretEntry.DoesNotExist:
        fs_connected = False
        fatsecret_status = "FatSecret не подключен"
    except GeneralError as error:
        fatsecret_status = f'При запросе к FatSecret возникла ошибка: {type(error)} - {error}'
        print('возникла GeneralError')
        print(error)
        print(type(error))

    # создание форм на основе записей в Measureforms
    for i in range(7):
        measure_date = date.today() - timedelta(days=i)
        try:
            # если запись за этот день есть, то формочка создается на ее основе
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)

        except Measurement.DoesNotExist:
            # если записи за этот день нет, то формочка создается пустая
            measure_form = MeasurementForm()

            # в нее сразу записывается user и дата
            measure_form = measure_form.save(commit=False)
            measure_form.user = request.user
            measure_form.date = measure_date
            # сохраняется запись в базе
            measure_form.save()

            # готовая форма на основе сущеcтсвующей пустой записи БД
            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)

        # перезапись кбжу в записях бд ЕСЛИ они изменились
        if fs_connected and food_data:
            # перевод даты в формат FS
            date_int = (measure_date - date(1970, 1, 1)).days
            # записываем кбжу в форму
            measure_form = measure_form.save(commit=False)
            # запись кбжу из FS для каждого дня
            # сортировать сначала по дате ?? (key=lambda x: x['date_int'])
            # food_data должна быть списком
            for day in food_data:
                if day['date_int'] == str(date_int):
                    # проверка на то, поменялись ли калории 
                    if measure_form.calories != int(day['calories']):
                        measure_form.calories = int(day['calories'])
                        measure_form.protein = float(day['protein'])
                        measure_form.fats = float(day['fat'])
                        measure_form.carbohydrates = float(day['carbohydrate'])
                        measure_form.save()
                    continue

            measure = Measurement.objects.get(date=measure_date, user=request.user)
            measure_form = MeasurementForm(instance=measure)

        week_measureforms.append(measure_form)

    # КАЛЕНДАРЬ для выбора даты
    week_calendar = []
    for i in range(7):
        selected_date = date.today() - timedelta(days=(6-i))
        week_calendar.append(selected_date)

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''
    
    # GET-запрос
    if request.method == 'GET':
        data = {
            'fatsecret_status': fatsecret_status,
            'week_measureforms': week_measureforms,
            'week_calendar': week_calendar,
            'today_commentary': today_commentary,
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
            # получаем вес из формы
            measure_weight = form.cleaned_data['weight']

            # ОТПРАВКА ВЕСА в FatSecret
            # дата измерения не старше 2 дней назад иначе FS не примет
            # и нельзя чтобы перезаписывалось на одну и ту же дату
            if fs_connected and measure_weight:
                if (date.today() - measure_date).days <= 2:
                    try:
                        try:
                            cur_month_weight = fs.weights_get_month()
                            last_date_weight = cur_month_weight[-1]['date_int']
                            last_date_weight = date(1970, 1 ,1) + timedelta(days=int(last_date_weight))
                            if last_date_weight < measure_date:
                                fs.weight_update(current_weight_kg=float(measure_weight),
                                                 date=datetime.combine(measure_date, time()))
                        except KeyError:
                            # если keyerror значит весов за этот месяц еще не внесено
                            if date.today().day >=3:
                                fs.weight_update(current_weight_kg=float(measure_weight),
                                                 date=datetime.combine(measure_date, time()))
                            else:
                                try:
                                    measure_month_weight = fs.weights_get_month(date=datetime.combine(measure_date, time()))
                                    last_date_weight = measure_month_weight[-1]['date_int']
                                    last_date_weight = date(1970, 1 ,1) + timedelta(days=int(last_date_weight))
                                    if last_date_weight < measure_date:
                                        fs.weight_update(current_weight_kg=float(measure_weight),
                                                         date=datetime.combine(measure_date, time()))
                                except KeyError:
                                    fs.weight_update(current_weight_kg=float(measure_weight),
                                                 date=datetime.combine(measure_date, time()))
                    except GeneralError as e:
                        # добавить инфо об ошибке на страницу!
                        print("Произошла ошибка при попытке отправки данных о весе в FatSecret:"
                            + str(type(e)) + str(e))

            # сохранение формы
            try:
                # получаем запись из БД с этим числом
                measure = Measurement.objects.get(date=measure_date, user=request.user) 
                # сформируем форму на ее основе и перезаписываем
                form = MeasurementForm(request.POST, instance=measure)
                form.save()
                return redirect('measurements')

            # если записи за число нет - это странно
            except Measurement.DoesNotExist:
                # перезагружаем с ошибкой
                data = {
                'week_measureforms': week_measureforms,
                'error': 'Случилось что-то непонятное, либо вы читерите :(',
                'week_calendar': week_calendar,
                'today_commentary': today_commentary,
                }
                return render(request, 'personalpage/addmeasure.html', data)

        # если форма некорректна - перезагружаем страницу с ошибкой
        else:
            data = {
                'fatsecret_status': fatsecret_status,
                'week_measureforms': week_measureforms,
                'error': 'Данные введены некорректно. Попробуйте еще раз.',
                'week_calendar': week_calendar,
                'today_commentary': today_commentary,
                }
            return render(request, 'personalpage/addmeasure.html', data)


def fatsecretauth(request):
    """Привязка к аккаунту FatSecret"""

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


def mealjournal(request):
    """Страница контроля питания и кбжу
    Тут отображается таблица за сегодняшний день
    и таблица за текущий месяц
    """
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    # GET-запрос
    if request.method == 'GET':

        try:
            # делаем сессию с FS для user
            make_session(request.user)
        except FatSecretEntry.DoesNotExist:
            # если FS не подключен - только предложение подключить
            data = {
                'user_not_connected': True,
                'today_commentary': today_commentary,
            }
            return render(request, 'personalpage/mealjournal.html', data)

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
            'food_entries_month': food_entries_month,
            'prods_without_info': prods_without_info,
            'avg_month': avg_month,
            'food_entry': food_entry,
            'day_total': day_total,
            'count_meal_in_category': count_meal_in_category,
            'today_day': today_day,
            'previous_month': previous_month,
            'user_not_connected': False,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/mealjournal.html', data)


def foodbydate(request):
    """Получение данных за опр.день из FatSecret
    С ТОПом по количеству и калориям
    """
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # делаем сессию с FS для user
    make_session(request.user)

    # получаем введенную дату
    briefdate = request.GET.get('date')
    if briefdate is None or not briefdate:
        return redirect('mealjournal')
    # форматируем для дальнейшей работы
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")
    # заготовки для html
    prev_date = str(briefdate - timedelta(days=1))[:10]
    next_date = str(briefdate + timedelta(days=1))[:10]

    # добавить обработчик too many actions!?

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    # ПИТАНИЕ за выбранную дату (briefdate)
    food_entry = fs.food_entries_get(date=briefdate)
    if not food_entry:
        data = {
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
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/foodbydate.html', data)

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
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/foodbydate.html', data)


def foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
       с кнопочкой подсчета ТОПов
    """
    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # делаем сессию с FS для user
    make_session(request.user)

     # месяц, за который нужно посчитать стату,
     # введенный на предыдущей странице
    briefmonth = request.GET.get('month')
    if briefmonth is None or not briefmonth:
        return redirect('mealjournal')

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

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    # создание ТОП-списков! (если нажать на кнопку)
    if request.GET.get('top_create', False):

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
        'today_commentary': today_commentary,
        }
    return render(request, 'personalpage/foodbymonth.html', data)


def anthropometry(request):
    """Страница внесения антропометрических измерений"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    # таблица сделанных измерений
    metrics = Anthropometry.objects.filter(user=request.user)
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
    
    # форма внесения новой записи
    metrics_form = AnthropometryForm()

    error = ""

    # комментарий за сегодня от эксперта
    try:
        today_commentary = Commentary.objects.get(date=date.today(), client=request.user)
    except Commentary.DoesNotExist:
        today_commentary = ''

    # сохранение полученной формы
    if request.method == 'POST':
        # получаем форму из запроса
        form = AnthropometryForm(request.POST, request.FILES)

        # проверяем на корректность
        if form.is_valid():
            # получаем дату из формы
            form_date = form.cleaned_data['date']

            if form_date <= date.today():
                try:
                    # если за это число есть - переписываем
                    exist_metrics = Anthropometry.objects.get(date=form_date,
                                                                user=request.user)                      
                    form = AnthropometryForm(request.POST, request.FILES, instance=exist_metrics)
                    form.save()
                except Anthropometry.DoesNotExist:
                    # сохраняем новую запись
                    form = form.save(commit=False)
                    form.user = request.user
                    form.save()
                return redirect('anthropometry')
        # если форма некорректна - перезагружаем страницу с ошибкой
        error = 'Введены некорректные данные'
        data = {
            'first_metrics': first_metrics,
            'prev_metrics': prev_metrics,
            'metrics_form': metrics_form,
            'metrics': metrics,
            'show_all': show_all,
            'error': error,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/anthropometry.html', data)

    # форма для настройки доступа к фото
    try:
        photoaccess_instance = UserSettings.objects.get(user=request.user)
    except UserSettings.DoesNotExist:
        photoaccess_instance = UserSettings.objects.create(user=request.user)

    photoaccess_form = PhotoAccessForm(instance=photoaccess_instance)
    # проверка текущей настройки достпуности фото
    accessibility = photoaccess_instance.photo_access

    data = {
        'first_metrics': first_metrics,
        'prev_metrics': prev_metrics,
        'metrics_form': metrics_form,
        'metrics': metrics,
        'show_all': show_all,
        'error': error,
        'photoaccess_form': photoaccess_form,
        'accessibility': accessibility,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/anthropometry.html', data)


def photoaccess_change(request):
    """Обработка изменения настройки доступа к фото в антропометрии"""
    # получаем форму из запроса
    form = PhotoAccessForm(request.POST)
    # проверяем на корректность
    if form.is_valid():
        # записываем значение в базу
        instance = UserSettings.objects.get(user=request.user)
        form = PhotoAccessForm(request.POST, instance=instance)
        form.save()

        accessible = form.cleaned_data['photo_access']
        data = {
            'accessible': accessible,
            }
        return JsonResponse(data, status=200)