from django.shortcuts import render, redirect
from measurements.forms import MeasurementForm
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from fatsecret_app.services import *
from measurements.services import *
from anthropometry.forms import AnthropometryForm
from anthropometry.services import *
from client_info.services import *
from expert_recommendations.services import *
from common.utils import get_noun_ending
from expert_remarks.services import get_today_commentary
from .utils import *


def personalpage(request):
    """Личный кабинет клиента"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username == 'Parrabolla':
        return redirect('expertpage')

    clientmemo_form = get_clientmemo_form_for(request.user)

    health_questionary_filled = is_health_questionary_filled_by(request.user)
    meet_questionary_filled = is_meet_questionary_filled_by(request.user)

    # контакты клиента
    contacts_filled = is_contacts_filled_by(request.user)
    contacts_form = get_contacts_form_for(request.user)

    #измерения за сегодня
    if user_has_fs_entry(request.user):
        renew_measure_nutrition(request.user, datetime.now())

    today_measure = get_daily_measure(request.user)

    # комментарий за сегодня от эксперта
    today_commentary = get_today_commentary(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
        'today_measure': today_measure,
        'health_questionary_filled': health_questionary_filled,
        'meet_questionary_filled': meet_questionary_filled,
        'contacts_form': contacts_form,
        'contacts_filled': contacts_filled,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/personalpage.html', data)


def client_settings(request):
    """Настройки клиента"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    clientmemo_form = get_clientmemo_form_for(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
    }

    return render(request, 'personalpage/settings.html', data)


def meet_questionary(request):
    """Страница заполнения анкеты знакомства"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    # открываем анкету
    if request.method == 'GET':

        clientmemo_form = get_clientmemo_form_for(request.user)
       
        meet_questionary = get_meet_questionary_of(request.user)
        meet_questionary_form = get_meet_questionary_form_for(request.user)
        readiness_choices = MeetQuestionary.READINESS_CHOICES
        age = get_age_int(request.user)
        today_commentary = get_today_commentary(request.user)

        data = {
            'clientmemo_form': clientmemo_form,
            'meet_questionary': meet_questionary,
            'meet_questionary_form': meet_questionary_form,
            'readiness_choices': readiness_choices,
            'age': age,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/meet_questionary.html', data)

    # сохраняем анкету
    if request.method == 'POST':

        form = MeetQuestionaryForm(request.POST)

        if form.is_valid():
            instance = get_meet_questionary_of(request.user)

            if instance:
                form = MeetQuestionaryForm(request.POST, instance=instance)
                form.save()
                return redirect('personalpage')
            else:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect('personalpage')

        else:
            clientmemo_form = get_clientmemo_form_for(request.user)
            meet_questionary = get_meet_questionary_of(request.user)
            meet_questionary_form = get_meet_questionary_form_for(request.user)
            readiness_choices = MeetQuestionary.READINESS_CHOICES
            age = get_age_int(request.user)
            today_commentary = get_today_commentary(request.user)

            data = {
                'clientmemo_form': clientmemo_form,
                'meet_questionary': meet_questionary,
                'meet_questionary_form': meet_questionary_form,
                'readiness_choices': readiness_choices,
                'age': age,
                'today_commentary': today_commentary,
                'error': 'Данные введены некорректно. Попробуйте ещё раз.',
            }
            return render(request, 'personalpage/meet_questionary.html', data)



def health_questionary(request):
    """Страница заполнения личной анкеты"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    # открываем анкету
    if request.method == 'GET':

        clientmemo_form = get_clientmemo_form_for(request.user)
       
        health_questionary = get_health_questionary_of(request.user)
        health_questionary_form = get_health_questionary_form_for(request.user)
        # комментарий за сегодня от эксперта
        today_commentary = get_today_commentary(request.user)

        data = {
            'clientmemo_form': clientmemo_form,
            'health_questionary': health_questionary,
            'health_questionary_form': health_questionary_form,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/health_questionary.html', data)

    # сохраняем анкету
    if request.method == 'POST':

        form = HealthQuestionaryForm(request.POST)

        if form.is_valid():
            instance = get_health_questionary_of(request.user)

            if instance:
                form = HealthQuestionaryForm(request.POST, instance=instance)
                form.save()
                return redirect('personalpage')
            else:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect('personalpage')

        else:
            clientmemo_form = get_clientmemo_form_for(request.user)
            health_questionary = get_health_questionary_of(request.user)
            health_questionary_form = get_health_questionary_form_for(request.user)
            today_commentary = get_today_commentary(request.user)

            data = {
                'clientmemo_form': clientmemo_form,
                'health_questionary': health_questionary,
                'health_questionary_form': health_questionary_form,
                'today_commentary': today_commentary,
                'error': 'Данные введены некорректно. Попробуйте ещё раз.',
            }
            return render(request, 'personalpage/health_questionary.html', data)


def measurements(request):
    """Страница отслеживания ежедневных измерений"""
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    if request.user.username == 'Parrabolla':
        return redirect('expertpage')

    clientmemo_form = get_clientmemo_form_for(request.user) 

    today_commentary = get_today_commentary(request.user)

    if user_has_fs_entry(request.user):
        renew_weekly_measures_nutrition(request.user)

    today_measure = get_daily_measure(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
        'today_measure': today_measure,
        'today_commentary': today_commentary,
    }

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

    return render(request, 'personalpage/measurements.html', data)    


def addmeasure(request):
    """Страница внесения и редактирования измерений"""
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    if request.method == 'GET':

        clientmemo_form = get_clientmemo_form_for(request.user)

        weekly_measure_forms = create_weekly_measure_forms(request.user)
        
        fatsecret_connected = user_has_fs_entry(request.user)
        if fatsecret_connected:
            renew_weekly_measures_nutrition(request.user)
            
        last_seven_dates = create_list_of_dates(7)
        today_commentary = get_today_commentary(request.user)       

        data = {
            'clientmemo_form': clientmemo_form,
            'fatsecret_connected': fatsecret_connected,
            'weekly_measure_forms': weekly_measure_forms,
            'last_seven_dates': last_seven_dates,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/addmeasure.html', data)

    if request.method == 'POST':

        clientmemo_form = get_clientmemo_form_for(request.user)

        fatsecret_connected = user_has_fs_entry(request.user)
        form = MeasurementForm(request.POST)
    
        if form.is_valid():
            measure_date = form.cleaned_data['date']
            measure_weight = form.cleaned_data['weight']

            if fatsecret_connected and measure_weight:
                set_weight_in_fatsecret(request.user, measure_weight, measure_date)

            instance = get_daily_measure(request.user, measure_date)

            if instance:
                form = MeasurementForm(request.POST, instance=instance)
                form.save()
                return redirect('measurements')
            else:
                addmeasure_error = 'Случилось что-то непонятное, либо вы читерите :('
        else:
            addmeasure_error = 'Данные введены некорректно. Попробуйте еще раз.'

        weekly_measure_forms = create_weekly_measure_forms(request.user)
        last_seven_dates = create_list_of_dates(7)
        today_commentary = get_today_commentary(request.user)    
        
        data = {
            'clientmemo_form': clientmemo_form,
            'addmeasure_error': addmeasure_error,
            'fatsecret_connected': fatsecret_connected,
            'weekly_measure_forms': weekly_measure_forms,
            'last_seven_dates': last_seven_dates,
            'today_commentary': today_commentary,
            }
        return render(request, 'personalpage/addmeasure.html', data)


def anthropometry(request):
    """Страница внесения антропометрических измерений"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    if request.method == 'GET':

        clientmemo_form = get_clientmemo_form_for(request.user)
        # сделанные измерения
        entries = get_anthropo_entries(request.user)

        # если запрошен полный список измерений
        if request.GET.get('show_all_entries'):
            show_all_entries = True
        else:
            show_all_entries = False

        # форма внесения новой записи
        new_entry_form = AnthropometryForm()
        # доступ эксперта к фото
        photoaccess_form = get_anthropo_photoaccess_form(request.user)
        photoaccess_allowed = photoaccess_form['photo_access'].value()
        # комментарий за сегодня от эксперта
        today_commentary = get_today_commentary(request.user)

        data = {
            'clientmemo_form': clientmemo_form,
            'entries': entries,
            'show_all_entries': show_all_entries,
            'new_entry_form': new_entry_form,
            'photoaccess_form': photoaccess_form,
            'photoaccess_allowed': photoaccess_allowed,
            'today_commentary': today_commentary,
        }
        return render(request, 'personalpage/anthropometry.html', data)

    # сохранение новых измерений
    if request.method == 'POST':

        form = AnthropometryForm(request.POST, request.FILES)

        if form.is_valid():
            entry_date = form.cleaned_data['date']
            instance = get_anthropo_entry(request.user, entry_date)

            if instance:
                form = AnthropometryForm(request.POST, request.FILES, instance=instance)
                form.save()
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
            return redirect('anthropometry')

        else:
            clientmemo_form = get_clientmemo_form_for(request.user)
            add_anthropo_error = 'Введены некорректные данные'

            # сделанные измерения
            entries = get_anthropo_entries(request.user)
            # форма внесения новой записи
            new_entry_form = AnthropometryForm()
            # доступ эксперта к фото
            photoaccess_form = get_anthropo_photoaccess_form(request.user)
            photoaccess_allowed = photoaccess_form['photo_access'].value()
            # комментарий за сегодня от эксперта
            today_commentary = get_today_commentary(request.user)

            data = {
                'clientmemo_form': clientmemo_form,
                'add_anthropo_error': add_anthropo_error,
                'entries': entries,
                'new_entry_form': new_entry_form,
                'photoaccess_form': photoaccess_form,
                'photoaccess_allowed': photoaccess_allowed,
                'today_commentary': today_commentary,
            }
            return render(request, 'personalpage/anthropometry.html', data)


def mealjournal(request):
    """Страница контроля питания и кбжу
    Тут отображается таблица за сегодняшний день за текущий месяц
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    clientmemo_form = get_clientmemo_form_for(request.user)

    # комментарий за сегодня от эксперта
    today_commentary = get_today_commentary(request.user)

    # проверяем, привязан ли у пользователя аккаунт Fatsecret
    if user_has_fs_entry(request.user) is False:
        # показываем предложение подключить
        data = {
            'clientmemo_form': clientmemo_form,
            'today_commentary': today_commentary,
            'user_not_connected': True,
        }
        return render(request, 'personalpage/mealjournal.html', data)
    else:
        # или делаем подсчеты
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
        # рекомендации кбжу
        recommend_nutrition = get_nutrition_recommend(request.user)

        data = {
            'clientmemo_form': clientmemo_form,
            'today_commentary': today_commentary,
            'daily_food': daily_food,
            'monthly_food': monthly_food,
            'prods_without_info': prods_without_info,
            'previous_month': previous_month,
            'recommend_nutrition': recommend_nutrition,
        }
        return render(request, 'personalpage/mealjournal.html', data)


def foodbydate(request):
    """Получение данных за опр.день из FatSecret
    С ТОП-3 по количеству и калориям
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    clientmemo_form = get_clientmemo_form_for(request.user)

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
    today_commentary = get_today_commentary(request.user)

    daily_food = count_daily_food(request.user, briefdate)
    daily_top = create_daily_top(request.user, briefdate)
    # рекомендации кбжу
    recommend_nutrition = get_nutrition_recommend(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
        'briefdate': briefdate,
        'prev_date': prev_date,
        'next_date': next_date,
        'daily_food': daily_food,
        'daily_top': daily_top,
        'today_commentary': today_commentary,
        'recommend_nutrition': recommend_nutrition,
    }
    return render(request, 'personalpage/foodbydate.html', data)


def foodbymonth(request):
    """Страница подробной статистики по КБЖУ за месяц из FatSecret
        с кнопочкой подсчета ТОП-10 продуктов
    """
    
    if request.user.is_anonymous:
        return redirect('loginuser')

    clientmemo_form = get_clientmemo_form_for(request.user)

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
    # рекомендации кбжу
    recommend_nutrition = get_nutrition_recommend(request.user)

    # комментарий за сегодня от эксперта
    today_commentary = get_today_commentary(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
        'briefmonth': month_datetime,
        'prev_month': prev_month,
        'next_month': next_month,
        'monthly_food': monthly_food,
        'today_commentary': today_commentary,
        'recommend_nutrition': recommend_nutrition,
    }
    return render(request, 'personalpage/foodbymonth.html', data)


def training(request):
    """Страница для контроля тренировок"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect('loginuser')
    if request.user.username == 'Parrabolla':
        return redirect('expertpage')

    clientmemo_form = get_clientmemo_form_for(request.user)

    # комментарий за сегодня от эксперта
    today_commentary = get_today_commentary(request.user)

    data = {
        'clientmemo_form': clientmemo_form,
        'today_commentary': today_commentary,
    }
    return render(request, 'personalpage/training.html', data)
