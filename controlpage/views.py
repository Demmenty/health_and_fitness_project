from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from fatsecret_app.services import *
from measurements.services import *
from anthropometry.services import *
from client_info.services import *
from expert_recommendations.services import *
from expert_remarks.services import get_remark_forms
from common.utils import get_noun_ending
from common.services import services


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
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    # дата регистрации
    date_joined = client.date_joined.date()

    # существоВание анкеты и возраст клиента
    health_questionary_filled = is_health_questionary_filled_by(client)
    meet_questionary_filled = is_meet_questionary_filled_by(client)
    client_height = get_height(client)
    client_age = get_age_string(client)

    # проверка подключения FatSecret
    fs_connected = services.fs.is_connected(client)
    # измерения за сегодня
    if fs_connected:
        renew_measure_nutrition(client, datetime.now())

    today_measure = get_daily_measure(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'health_questionary_filled': health_questionary_filled,
        'meet_questionary_filled': meet_questionary_filled,
        'fs_connected': fs_connected,
        'today_measure': today_measure,
        'client_age': client_age,
        'client_height': client_height,
        'date_joined': date_joined,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
    }
    return render(request, 'controlpage/client_mainpage.html', data)


def client_health_questionary(request):
    """Анкета здоровья клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)

    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)
    # анкета здоровья
    health_questionary = get_health_questionary_of(client)
    health_questionary_form = get_health_questionary_form_for(client)
    
    data = {
        'clientname': client.username,
        'client_id': client_id,
        'health_questionary': health_questionary,
        'health_questionary_form': health_questionary_form,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
    }
    return render(request, 'controlpage/client_health_questionary.html', data)


def client_meet_questionary(request):
    """Анкета здоровья клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)

    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)
    # анкета здоровья
    meet_questionary = get_meet_questionary_of(client)
    meet_questionary_form = get_meet_questionary_form_for(client)
    readiness_choices = MeetQuestionary.READINESS_CHOICES
    
    data = {
        'clientname': client.username,
        'client_id': client_id,
        'meet_questionary': meet_questionary,
        'meet_questionary_form': meet_questionary_form,
        'readiness_choices': readiness_choices,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
    }
    return render(request, 'controlpage/client_meet_questionary.html', data)


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
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    # настройки цветовых фонов для показателей клиента
    colorsettings_exist = user_has_measeurecolor_settings(client)
    colorset_forms = create_colorset_forms(client)
    # указанное в анкете нормальное давление
    normal_pressure = get_normal_pressure_of(client)

    # измерения клиента
    if services.fs.is_connected(client):
        renew_weekly_measures_nutrition(client)
    # измерения за сегодня
    today_measure = get_daily_measure(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
        'today_measure': today_measure,
        'colorsettings_exist': colorsettings_exist,
        'colorset_forms': colorset_forms,
        'normal_pressure': normal_pressure,
    }

    # измерения за период дней
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

    return render(request, 'controlpage/client_measurements.html', data)


def client_anthropometry(request):
    """Антропометрические данные клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    # сделанные измерения антропометрии
    entries = get_anthropo_entries(client)

    # если запрошен полный список измерений
    if request.GET.get('show_all_entries'):
        show_all_entries = True
    else:
        show_all_entries = False

    # проверка текущей настройки достпуности фото
    photoaccess_allowed = is_photoaccess_allowed(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
        'entries': entries,
        'show_all_entries': show_all_entries, 
        'photoaccess_allowed': photoaccess_allowed,
    }
    return render(request, 'controlpage/client_anthropometry.html', data)


def client_mealjournal(request):
    """Страница контроля питания и кбжу клиента.
    Тут отображаются таблицы за сегодняшний день и за текущий месяц
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
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
    }

    # проверяем, привязан ли у пользователя аккаунт Fatsecret
    if services.fs.is_connected(client) is False:
        # показываем уведомление
        data.update({
            'client_not_connected': True,
        })
        return render(request, 'controlpage/client_mealjournal.html', data)  
    else:
        # делаем подсчеты
        daily_food = services.fs.daily_food(client, datetime.today())
        monthly_food = services.fs.monthly_food(client, datetime.today())

        # словарь продуктов, для которых нет инфо о граммовке порции
        prods_without_info = {}
        if daily_food.get('without_info'):
            prods_without_info.update(daily_food['without_info'])
        if monthly_food.get('without_info'):
            prods_without_info.update(monthly_food['without_info'])

        # для поля выбора (потом сделать через js)
        previous_month = date.today() + relativedelta(months=-1)
        previous_month = previous_month.strftime("%Y-%m")
        # рекомендации кбжу
        recommend_nutrition_form = get_nutrition_recommend_form(client)
    
        data.update({
            'daily_food': daily_food,
            'monthly_food': monthly_food,
            'prods_without_info': prods_without_info,
            'previous_month': previous_month,
            'recommend_nutrition_form': recommend_nutrition_form,
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

    # получаем введенную дату, проверяем, форматируем
    briefdate = request.GET.get('date')
    if not briefdate:
        return redirect('mealjournal')
    briefdate = datetime.strptime(briefdate, "%Y-%m-%d")

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    # для подстановки в html (пока так, потом в js)
    prev_date = briefdate - timedelta(days=1)
    next_date = briefdate + timedelta(days=1)
    prev_date = prev_date.strftime("%Y-%m-%d")
    next_date = next_date.strftime("%Y-%m-%d")

    daily_food = services.fs.daily_food(client, briefdate)
    daily_top = services.fs.daily_top(client, briefdate)
    recommend_nutrition_form = get_nutrition_recommend_form(client)  

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
        'briefdate': briefdate,
        'prev_date': prev_date,
        'next_date': next_date,
        'daily_food': daily_food,
        'daily_top': daily_top, 
        'recommend_nutrition_form': recommend_nutrition_form, 
    }
    return render(request, 'controlpage/client_foodbydate.html', data)


def client_foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
       с кнопочкой подсчета ТОП-10 продуктов
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')

    # получаем введенный месяц, проверяем, форматируем
    month_str = request.GET.get('month')
    if month_str is None or not month_str:
        return redirect('mealjournal')
    month_datetime = datetime.strptime(month_str, "%Y-%m")

    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    # для подстановки в html (пока так)
    prev_month = month_datetime + relativedelta(months=-1)
    next_month = month_datetime + relativedelta(months=1)
    prev_month = prev_month.strftime("%Y-%m")
    next_month = next_month.strftime("%Y-%m") 

    monthly_food = services.fs.monthly_food(client, month_datetime)
    recommend_nutrition_form = get_nutrition_recommend_form(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
        'briefmonth': month_datetime,
        'prev_month': prev_month,
        'next_month': next_month,
        'monthly_food': monthly_food,
        'recommend_nutrition_form': recommend_nutrition_form,
    }
    return render(request, 'controlpage/client_foodbymonth.html', data)


def client_training(request):
    """Cтраница контроля за тренировками клиентом"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username != 'Parrabolla':
        return redirect('homepage')
    
    # определение клиента
    client_id = request.GET['client_id']
    client = User.objects.get(id=client_id)
    
    # контакты клиента
    client_contacts = get_contacts_of(client)
    # комментарий и заметки
    client_remark = get_remark_forms(client)

    data = {
        'clientname': client.username,
        'client_id': client_id,
        'client_contacts': client_contacts,
        'client_remark': client_remark,
    }
    return render(request, 'controlpage/client_training.html', data)
    