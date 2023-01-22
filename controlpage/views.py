import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from personalpage.models import  Questionary, Anthropometry, UserSettings
from controlpage.models import Commentary, Clientnote, FullClientnote
from personalpage.forms import QuestionaryForm
from controlpage.forms import CommentaryForm, ClientnoteForm, FullClientnoteForm
from time import sleep
from itertools import zip_longest
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from personalpage.views import get_avg_for_period
from fatsecret import Fatsecret, GeneralError
from django.http import JsonResponse
from fatsecret_app.services import *
from measurements.services import *
from .comments_services import *


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


def get_client_contacts(client):
    """Достаем контакты клиента из его настроек"""
    try:
        instance = UserSettings.objects.get(user=client)

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


def get_age(birthdate):
    """получить количество полных лет по дню рождения"""
    now = date.today()
    age = now.year - birthdate.year
    if (now.month < birthdate.month or
       (now.month == birthdate.month and now.day < birthdate.day)):
        age = age - 1
    return age
   


# Аякс-запросы
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


def get_clientnote_form(request):
    """Получение формы коммента клиенту для эксперта
       для выбранной на странице даты через скрипт в layout"""

    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    print(request.GET)

    client_id = request.GET['client_id']
    clientnote_date = request.GET['date'] + '-01'

    try:
        instance = Clientnote.objects.get(client=client_id, date=clientnote_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
        }
    except Clientnote.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        }

    return JsonResponse(data, status=200)


def save_clientnote_form(request):
    """Сохранение формы заметки о клиенте через аякс-скрипт"""
    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        client_id = request.POST['client']
        form = ClientnoteForm(request.POST)

        if form.is_valid():
            clientnote_date = form.cleaned_data['date']
            try:
                instance = Clientnote.objects.get(client=client_id, date=clientnote_date)
                form = ClientnoteForm(request.POST, instance=instance)
                form.save()
            except Clientnote.DoesNotExist:
                form.save()
            result = 'заметка сохранена'
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)
    

def save_full_clientnote_form(request):
    """Сохранение формы совокупной заметки о клиенте через аякс-скрипт"""
    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        client_id = request.POST['client']
        form = FullClientnoteForm(request.POST)

        if form.is_valid():
            try:
                instance = FullClientnote.objects.get(client=client_id)
                form = FullClientnoteForm(request.POST, instance=instance)
                form.save()
            except FullClientnote.DoesNotExist:
                form.save()
            result = 'заметка сохранена'
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)
    

# My views
def client_mainpage(request):
    """Главная страница контроля за клиентом
     - аналог personalpage, но для эксперта"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    # дата регистрации
    date_joined = client.date_joined.date()

    # существоВание анкеты и возраст клиента
    questionary = Questionary.objects.filter(user=client).first()
    if questionary:
        client_age = get_age(questionary.birth_date)
        client_age_str = (str(client_age) + ' ' +
                    get_noun_ending(client_age, 'год', 'года', 'лет'))
    else:
        client_age_str = 'неизвестно'

    # проверка подключения FatSecret
    fs_connected = user_has_fs_entry(client)

    # измерения за сегодня
    if user_has_fs_entry(client):
        renew_measure_nutrition(client, datetime.now())
    today_measure = get_daily_measure(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'questionary': questionary,
        'fs_connected': fs_connected,
        'today_measure': today_measure,
        'client_age': client_age_str,
        'date_joined': date_joined,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }
    return render(request, 'controlpage/client_mainpage.html', data)


def client_questionary(request):
    """Анкета клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    questionary = Questionary.objects.filter(user=client).first()
    questionary_form = QuestionaryForm()
    
    data = {
        'clientname': client.username,
        'client_id': client_id,
        'questionary': questionary,
        'form': questionary_form,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }
    return render(request, 'controlpage/client_questionary.html', data)


def client_measurements(request):
    """Страница отслеживания ежедневных измерений"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }

    # измерения клиента
    if user_has_fs_entry(client):
        renew_weekly_measures_nutrition(client)

    today_measure = get_daily_measure(client)

    if request.GET.get('selectperiod'):
        period = int(request.GET['selectperiod'])
    else:
        period = 7
    period_measures = get_last_measures(client, days=period)

    if period_measures:
        period_measures_avg = create_avg_for_measures(period_measures)
        period_measure_comment_forms = get_measure_comment_forms(period_measures)
        period_as_string = f"{period} {get_noun_ending(period, 'день', 'дня', 'дней')}"
        need_to_show_pressure = bool(period_measures_avg.get('pressure'))

        data.update({     
            'period_measures': period_measures,
            'period_measures_avg': period_measures_avg,
            'period_measure_comment_forms': period_measure_comment_forms,
            'period_as_string': period_as_string,
            'need_to_show_pressure': need_to_show_pressure,
        })

    # настройки цветовых фонов для показателей клиента
    colorsettings_exist = user_has_measeurecolor_settings(client)
    colorset_forms = create_colorset_forms(client)

    # указанное в анкете нормальное давление
    questionary = Questionary.objects.filter(user=client).first()
    if not questionary:
        norm_pressure = 'не заполнено'
    elif questionary.norm_pressure == 'no':
        norm_pressure = 'не знает'
    else:
        norm_pressure = questionary.norm_pressure
    
    data.update({
        'today_measure': today_measure,
        'colorsettings_exist': colorsettings_exist,
        'colorset_forms': colorset_forms,
        'norm_pressure': norm_pressure,
    })
    return render(request, 'controlpage/client_measurements.html', data)


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

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }

    # проверяем, привязан ли у пользователя аккаунт Fatsecret
    if user_has_fs_entry(client) is False:
        # показываем уведомление
        data.update({
            'client_not_connected': True,
        })
        return render(request, 'controlpage/client_mealjournal.html', data)  
    else:
        # делаем подсчеты
        daily_food = count_daily_food(client, datetime.today())
        monthly_food = count_monthly_food(client, datetime.today())

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
        return render(request, 'controlpage/client_mealjournal.html', data)   


def client_foodbydate(request):
    """Получение данных за опр.день из FatSecret
    С ТОП-3 по количеству и калориям
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }

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

    daily_food = count_daily_food(client, briefdate)
    daily_top = create_daily_top(client, briefdate)  

    data.update({
        'briefdate': briefdate,
        'prev_date': prev_date,
        'next_date': next_date,
        'daily_food': daily_food,
        'daily_top': daily_top,  
    })
    return render(request, 'controlpage/client_foodbydate.html', data)


def client_foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
       с кнопочкой подсчета ТОП-10 продуктов
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_client_contacts(client)
    # комментарий для клиента
    client_comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    clientnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    full_clientnote_form = get_full_clientnote_form(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_comment_form': client_comment_form,
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }

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

    monthly_food = count_monthly_food(client, month_datetime)

    data.update({
        'briefmonth': month_datetime,
        'prev_month': prev_month,
        'next_month': next_month,
        'monthly_food': monthly_food,
    })
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
    # заметка о клиенте
    clientnote_form = today_clientnote_form(client_id)
    # заметка о клиенте совокупная
    try:
        instance = FullClientnote.objects.get(client=client_id)
        full_clientnote_form = FullClientnoteForm(instance=instance)
    except FullClientnote.DoesNotExist:
        full_clientnote_form = FullClientnoteForm()

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
        'clientnote_form': clientnote_form,
        'full_clientnote_form': full_clientnote_form,
    }
    return render(request, 'controlpage/client_anthropometry.html', data)