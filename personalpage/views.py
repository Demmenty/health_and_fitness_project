from django.shortcuts import render, redirect
from .models import Anthropometry, Questionary, UserSettings
from controlpage.models import Commentary
from django.db.models import Q
from .forms import AnthropometryForm, QuestionaryForm, PhotoAccessForm, ContactsForm
from measurements.forms import MeasurementForm, MeasurementCommentForm
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from fatsecret_app.services import *
from measurements.services import *


# внутренние функции
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


def get_avg_for_period(user_id, period=7):
    """Составляет словарь из средних значений по
       каждому ежедневному измерению физичских показателей за неделю.
       Нужно передать user_id и period=кол-во дней
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


# Аякс-запросы
def get_expert_commentary(request):
    """Получение формы коммента клиенту для клиента
       для выбранной на странице даты через скрипт в layout"""
    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    client_id = request.user.id
    comment_date = request.GET['date']

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

    if request.user.is_anonymous:
        return redirect('loginuser')

    prods_without_info = dict(request.POST)
    del prods_without_info['csrfmiddlewaretoken']

    save_foodmetric_into_foodcache(prods_without_info)

    data = {'status': "инфа сохранена, круто!"}
    return JsonResponse(data, status=200)
  

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


# My views
def personalpage(request):
    """Личный кабинет клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username == 'Parrabolla':
        return redirect('expertpage')

    questionary = Questionary.objects.filter(user=request.user).first()

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
    today_measure = get_daily_measure(request.user)
    renew_measure_nutrition(request.user, datetime.now())

    # комментарий за сегодня от эксперта
    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()

    data = {
        'today_measure': today_measure,
        'questionary': questionary,
        'contacts_form': contacts_form,
        'contacts_error': contacts_error,
        'contacts_filled': contacts_filled,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/personalpage.html', data)


def questionary(request):
    """Страница заполнения личной анкеты"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    # комментарий за сегодня от эксперта
    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()

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


def measurements(request):
    """Страница отслеживания ежедневных измерений"""
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    if request.user.username == 'Parrabolla':
        return redirect('expertpage') 

    data = {}

    if user_has_fs_entry(request.user):
        renew_weekly_measures_nutrition(request.user)

    today_measure = get_daily_measure(request.user)

    if request.GET.get('selectperiod'):
        period = int(request.GET['selectperiod'])
    else:
        period = 7

    period_measures = get_last_measures(request.user, days=period)

    if period_measures:
        period_measures_avg = create_avg_for_measures(period_measures)
        period_measure_comment_forms = get_measure_comment_forms(period_measures)
        period_as_string = f"{period} {get_noun_ending(period, 'день', 'дня', 'дней')}"
        need_to_show_pressure = bool(period_measures_avg.get('pressure'))

        colorsettings_exist = user_has_measeurecolor_settings(request.user)

        data.update({     
            'period_measures': period_measures,
            'period_measures_avg': period_measures_avg,
            'period_measure_comment_forms': period_measure_comment_forms,
            'period_as_string': period_as_string,
            'need_to_show_pressure': need_to_show_pressure,
            'colorsettings_exist': colorsettings_exist,
        })

    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()

    data.update({
        'today_measure': today_measure,
        'today_commentary': today_commentary,
    })
    return render(request, 'personalpage/measurements.html', data)    


def addmeasure(request):
    """Страница внесения и редактирования измерений"""
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    fatsecret_connected = user_has_fs_entry(request.user)

    if request.method == 'GET':

        if fatsecret_connected:
            renew_weekly_measures_nutrition(request.user)
            
        weekly_measure_forms = create_weekly_measure_forms(request.user)

        last_seven_dates = []
        for i in range(7):
            selected_date = date.today() - timedelta(days=(6-i))
            last_seven_dates.append(selected_date)

        today_commentary = Commentary.objects.filter(
                date=date.today(), client=request.user).first()        

        data = {
            'fatsecret_connected': fatsecret_connected,
            'weekly_measure_forms': weekly_measure_forms,
            'last_seven_dates': last_seven_dates,
            'today_commentary': today_commentary,
            }
        return render(request, 'personalpage/addmeasure.html', data)

    if request.method == 'POST':

        form = MeasurementForm(request.POST)
    
        if form.is_valid():

            measure_date = form.cleaned_data['date']
            measure_weight = form.cleaned_data['weight']

            if fatsecret_connected and measure_weight:
                set_weight_in_fatsecret(request.user, measure_weight, measure_date)

            instance = Measurement.objects.filter(
                        date=measure_date, user=request.user).first()

            if instance:
                form = MeasurementForm(request.POST, instance=instance)
                form.save()
                return redirect('measurements')
            else:
                error = 'Случилось что-то непонятное, либо вы читерите :('
        else:
            error = 'Данные введены некорректно. Попробуйте еще раз.'

        weekly_measure_forms = create_weekly_measure_forms(request.user)

        last_seven_dates = []
        for i in range(7):
            selected_date = date.today() - timedelta(days=(6-i))
            last_seven_dates.append(selected_date)

        today_commentary = Commentary.objects.filter(
                date=date.today(), client=request.user).first()     
        
        data = {
            'error': error,
            'fatsecret_connected': fatsecret_connected,
            'weekly_measure_forms': weekly_measure_forms,
            'last_seven_dates': last_seven_dates,
            'today_commentary': today_commentary,
            }
        return render(request, 'personalpage/addmeasure.html', data)


def mealjournal(request):
    """Страница контроля питания и кбжу
    Тут отображается таблица за сегодняшний день за текущий месяц
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    # комментарий за сегодня от эксперта
    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()
    
    data = {'today_commentary': today_commentary,}

    # проверяем, привязан ли у пользователя аккаунт Fatsecret
    if user_has_fs_entry(request.user) is False:
        # показываем предложение подключить
        data.update({
            'user_not_connected': True,
        })
        return render(request, 'personalpage/mealjournal.html', data)
    else:
        # делаем подсчеты
        daily_food = count_daily_food(request.user, datetime.today())
        monthly_food = count_monthly_food(request.user, datetime.today())

        # словарь продуктов, для которых нет инфо о граммовке порции
        prods_without_info = {}
        if daily_food.get('without_info'):
            prods_without_info.update(daily_food['without_info'])
        if monthly_food.get('without_info'):
            prods_without_info.update(monthly_food['without_info'])

        # для поля выбора (потом сделать через js)
        previous_month = date.today() + relativedelta(months=-1)
        previous_month = previous_month.strftime("%Y-%m")

        data.update({
            'daily_food': daily_food,
            'monthly_food': monthly_food,
            'prods_without_info': prods_without_info,
            'previous_month': previous_month,
        })
        return render(request, 'personalpage/mealjournal.html', data)


def foodbydate(request):
    """Получение данных за опр.день из FatSecret
    С ТОП-3 по количеству и калориям
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    # получаем введенную дату, проверяем, форматируем
    briefdate = request.GET.get('date')
    if not briefdate:
        return redirect('mealjournal')
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")

    # для подстановки в html (пока так)
    prev_date = briefdate - timedelta(days=1)
    next_date = briefdate + timedelta(days=1)
    prev_date = prev_date.strftime("%Y-%m-%d")
    next_date = next_date.strftime("%Y-%m-%d")

    # комментарий за сегодня от эксперта
    today_commentary = Commentary.objects.filter(
        date=date.today(), client=request.user).first()

    daily_food = count_daily_food(request.user, briefdate)
    daily_top = create_daily_top(request.user, briefdate)

    data = {
        'briefdate': briefdate,
        'prev_date': prev_date,
        'next_date': next_date,
        'daily_food': daily_food,
        'daily_top': daily_top,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/foodbydate.html', data)


def foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
        с кнопочкой подсчета ТОП-10 продуктов
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    # месяц, за который нужно посчитать стату,
    # введенный на предыдущей странице
    month_str = request.GET.get('month')

    if month_str is None or not month_str:
        return redirect('mealjournal')

    month_datetime = datetime.strptime(month_str, "%Y-%m")

    # для подстановки в html (пока так)
    prev_month = month_datetime + relativedelta(months=-1)
    next_month = month_datetime + relativedelta(months=1)
    prev_month = prev_month.strftime("%Y-%m")
    next_month = next_month.strftime("%Y-%m")
    
    monthly_food = count_monthly_food(request.user, month_datetime)

    # комментарий за сегодня от эксперта
    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()

    data = {
        'briefmonth': month_datetime,
        'prev_month': prev_month,
        'next_month': next_month,
        'monthly_food': monthly_food,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/foodbymonth.html', data)


def anthropometry(request):
    """Страница внесения антропометрических измерений"""

    
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
    today_commentary = Commentary.objects.filter(
            date=date.today(), client=request.user).first()

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
