from fatsecret import Fatsecret
from fatsecret import ParameterError as FS_ParameterError, GeneralError as FS_GeneralError
from django.conf import settings
from .models import FatSecretEntry
import pickle
from datetime import date, datetime, time, timedelta
# from time import sleep
from common.utils import datetime_into_epoch, epoch_into_datetime


# сессии
def create_common_fs_session():
    """возвращает клиент API для взаимодействия с FatSecret приложением"""
    fs_session = Fatsecret(
        settings.FS_CONSUMER_KEY,
        settings.FS_CONSUMER_SECRET)

    return fs_session


def create_user_fs_session(user):
    """возвращает клиент API для взаимодействия с FatSecret приложением
    для конкретного пользователя"""

    userdata = FatSecretEntry.objects.get(user=user)
    session_token = (userdata.oauth_token, userdata.oauth_token_secret)
    fs_session = Fatsecret(
        settings.FS_CONSUMER_KEY,
        settings.FS_CONSUMER_SECRET,
        session_token=session_token)

    return fs_session


def save_session_token(session_token, user) -> None:
    """сохранение токена для взаимодействия с FS в базе данных"""

    FatSecretEntry.objects.get_or_create(
        user=user,
        oauth_token=session_token[0],
        oauth_token_secret=session_token[1])


def user_has_fs_entry(user) -> bool:
    """Проверяет, привязан ли у пользователя аккаунт Fatsecret"""

    return FatSecretEntry.objects.filter(user=user).exists()


# получение данных
def get_daily_nutrition_fs(user, request_date: datetime) -> dict:
    """получение словаря с кбжу из FS за запрошенный день"""

    fs_session = create_user_fs_session(user)

    monthly_nutrition = fs_session.food_entries_get_month(date=request_date)

    if not monthly_nutrition:
        return {}

    for day in monthly_nutrition:
        if day['date_int'] == datetime_into_epoch(request_date):
            return day


def get_weekly_nutrition_fs(user) -> dict:
    """получение словаря с кбжу из FS за последние 7 дней
    ключи словаря - date_int:str"""

    fs_session = create_user_fs_session(user)

    week_nutrition_list = []

    # получаем данные по текущему месяцу
    current_month_nutrition = fs_session.food_entries_get_month()
    if type(current_month_nutrition) is dict:
        week_nutrition_list += [current_month_nutrition]
    else:
        week_nutrition_list += current_month_nutrition

    # если сегодня 6 число или меньше, добавить и предыдущий месяц
    if date.today().day < 7:
        previous_month_nutrition = fs_session.food_entries_get_month(
                            date=datetime.today() - timedelta(weeks=4))
        if type(previous_month_nutrition) is dict:
            week_nutrition_list += [previous_month_nutrition]
        else:
            week_nutrition_list += previous_month_nutrition

    # фильтруем новейшие 7 записей
    week_nutrition_list = sorted(
                week_nutrition_list,
                key=lambda x: x['date_int'],
                reverse=True)[:7]

    # превращаем в словарь с ключами = date_int
    week_nutrition_dic = {}
    for day in week_nutrition_list:
        week_nutrition_dic[day['date_int']] = day
        del week_nutrition_dic[day['date_int']]['date_int']

    return week_nutrition_dic


# отправка в Fatsecret
def set_weight_in_fatsecret(user, measure_weight: str, measure_date: date) -> None:
    """отправка показателя веса клиента в аккаунт приложения fatsecret.
    вес записывается, только, если еще нет записи за этот день или свежее"""

    try:
        fs_session = create_user_fs_session(user)

        measure_weight = float(measure_weight)
        measure_datetime = datetime.combine(measure_date, time())
        measure_date_int = datetime_into_epoch(measure_datetime)

        # проверяем существующие внесения веса в fatsecret
        monthly_weights = fs_session.weights_get_month()

        if monthly_weights:
            if type(monthly_weights) is dict:
                last_record_date_int = monthly_weights['date_int']
            else:
                last_record_date_int = monthly_weights[-1]['date_int']

            if last_record_date_int < measure_date_int:
                fs_session.weight_update(
                        current_weight_kg=measure_weight,
                        date=measure_datetime)
        else:
            fs_session.weight_update(
                    current_weight_kg=measure_weight,
                    date=measure_datetime)

    except FS_GeneralError as error:
        print("Произошла ошибка при попытке отправки данных о весе в FatSecret:"
            + str(type(error)) + str(error))


# подсчеты
def count_daily_food(user, request_date:datetime) -> dict:
    """Подсчитывает данные о съеденных продуктах за день
    вывод - словарь:
    'entries' - список словарей с позициями еды, датой и кбжу
    'nutrition' - общее кбжу за день
    'count_by_category' - сколько в ужин, обед и тп
    'without_info' - продукты без метрики
    """

    fs_session = create_user_fs_session(user)

    daily_entries = fs_session.food_entries_get(date=request_date)

    if not daily_entries:
        return {}

    # продукты, для которых нет инфо о граммовке порции
    without_info = {}

    # категории для таблички
    count_by_category = {
        'Breakfast': 0,
        'Lunch': 0,
        'Dinner': 0,
        'Other': 0,
        }
    # итоговые кбжу дня
    nutrition = {
        'amount': 0,
        'calories': 0,
        'protein': 0,
        'fat': 0,
        'carbohydrate': 0,
        }

    # складываем одинаковую еду в этот словарик (для топов)
    daily_total = {}
    # для понимания, можно сохранить итог, или нет
    daily_total_is_good = True

    # обработка каждой записи о продукте
    for food in daily_entries:

        # подсчет количеств блюд для каждой категории для таблички
        count_by_category[food['meal']] += 1
        # поиск подробностей о продукте для подсчета порции
        food_info = _get_foodinfo_from_foodcache(food['food_id'])
        food_info_found = True
        if not food_info:
            print('запрос food_info из fs')
            try:
                food_info = fs_session.food_get(food_id=food['food_id'])
                _save_foodinfo_into_foodcache(food_info)
            except FS_ParameterError:
                food_info_found = False
                food['cant_get_id'] = True
                daily_total_is_good = False
                
        if food_info_found:
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
                nutrition['amount'] += food['norm_amount']
            else:
                # если измерение в порциях - сначала проверяем, есть ли граммовка порции
                if food['serving'].get('metric_serving_amount') is None:
                    # если в инфе не оказалось граммовки порции
                    # добавляем эту еду в спец.словарь и не считаем amount
                    daily_total_is_good = False
                    without_info[food['food_id']] = {
                        'food_entry_name': food['food_entry_name'],
                        'serving_description': food['serving'].get('serving_description', 'порция'),
                        'serving_id': food['serving_id'],
                        'calories_per_serving': int(int(food['calories']) / float(food['number_of_units']))
                    }
                else:
                    # если в инфе метрика есть - считаем и добавляем к общему подсчету
                    food['norm_amount'] = int(float(food['number_of_units']) *
                                            float(food['serving']['metric_serving_amount']) *
                                            float(food['serving']['number_of_units']))
                    nutrition['amount'] += food['norm_amount']

        # подсчет итоговой суммы кбжу
        nutrition['calories'] += int(food['calories'])
        nutrition['protein'] += float(food['protein'])
        nutrition['fat'] += float(food['fat'])
        nutrition['carbohydrate'] += float(food['carbohydrate'])

        # заодно готовим daily_total
        # меняем наименование на то, что в инфе, оно более общее
        if food_info_found:
            food['food_name'] = food_info['food_name']
        else:
            food['food_name'] = food['food_entry_name']
        # складываем у продуктов с одинаковым именем калории и вес
        if daily_total.get(food['food_name']) is None:
            daily_total[food['food_name']] = {
                'calories': 0,
                'amount': 0,
            }
        daily_total[food['food_name']]['calories'] += int(food['calories'])
        # если получилось высчитать нормально количество
        # (если нет - то продукт в списке without_info, либо не имеет такого ключа)
        if food.get('norm_amount'):
            daily_total[food['food_name']]['amount'] += food['norm_amount']
            daily_total[food['food_name']]['metric'] = food['serving']['metric_serving_unit']

    # округляем результаты в получившемся итоге по кбжу
    for key, value in nutrition.items():
        nutrition[key] = round(value, 2)

    # сохраняем daily_total в кеше на будущее для топов
    if daily_total_is_good:
        _save_daily_total_in_cache(user, request_date, daily_total)

    # добавить очистку от ненужных значений??

    return {
        'entries': daily_entries,
        'nutrition': nutrition,
        'count_by_category': count_by_category,
        'without_info': without_info,
    }


def count_monthly_food(user, request_date) -> dict:
    """Подсчитывает данные о съеденных продуктах за месяц
    возвращает словарь
    'entries' - список словарей по дням с кбжу,
    'monthly_avg' - словарь со средними кбжу"""

    fs_session = create_user_fs_session(user)

    # средние показатели кбжу
    monthly_avg = {
        'protein': 0,
        'fat': 0,
        'carbo': 0,
        'calories': 0
    }

    monthly_entries = fs_session.food_entries_get_month(date=request_date)
    if not monthly_entries:
        return {}

    # если за месяц одна запись - у fs будет просто словарь
    if type(monthly_entries) is dict:
        monthly_entries = [monthly_entries]

    days_count = len(monthly_entries)

    for day in monthly_entries:
        day['date_datetime'] = date(1970, 1, 1) + timedelta(days=int(day['date_int']))
        monthly_avg['protein'] += float(day['protein'])
        monthly_avg['fat'] += float(day['fat'])
        monthly_avg['carbo'] += float(day['carbohydrate'])
        monthly_avg['calories'] += float(day['calories'])
    monthly_avg['protein'] = round(monthly_avg['protein'] / days_count, 2)
    monthly_avg['fat'] = round(monthly_avg['fat'] / days_count, 2)
    monthly_avg['carbo'] = round(monthly_avg['carbo'] / days_count, 2)
    monthly_avg['calories'] = round(monthly_avg['calories'] / days_count, 2)

    return {
        'entries': monthly_entries,
        'monthly_avg': monthly_avg,
    }


# топы
def create_daily_top(user, entry_date: datetime) -> dict:
    """создание топ-3 продуктов за месяц, по весу и по калориям"""

    daily_total = _get_daily_total_from_cache(user, entry_date)

    if not daily_total:
        daily_total = _create_daily_total(user, entry_date)
        _save_daily_total_in_cache(user, entry_date, daily_total)

    daily_top = {}

    if daily_total.get('without_info'):
        daily_top['without_info'] = daily_total['without_info']
        del daily_total['without_info']

    top_calories = dict(sorted(
            daily_total.items(),
            key=lambda x: x[1]['calories'],
            reverse=True)[:3])

    top_amount = dict(sorted(
            daily_total.items(),
            key=lambda x: x[1]['amount'],
            reverse=True)[:3])

    daily_top.update({'top_calories': top_calories,
                      'top_amount': top_amount})

    return daily_top

    
def create_monthly_top(user, month: datetime) -> dict:
    """создание топ-10 продуктов за месяц, по весу и по калориям"""

    monthly_total = _get_monthly_total_from_cache(user, month)

    if not monthly_total:
        print('monthly_total в кеше нет')
        monthly_total = _create_monthly_total(user, month)

        if monthly_total.get('without_info') is None:
            _save_monthly_total_in_cache(user, month, monthly_total)

    monthly_top = {}

    if monthly_total.get('without_info'):
        monthly_top['without_info'] = monthly_total['without_info']
        del monthly_total['without_info']
    
    top_calories = dict(sorted(
        monthly_total.items(),
        key=lambda x: x[1]['calories'],
        reverse=True)[:10])

    top_amount = dict(sorted(
        monthly_total.items(),
        key=lambda x: x[1]['amount'],
        reverse=True)[:10])

    monthly_top.update({'top_calories': top_calories,
                        'top_amount': top_amount})

    return monthly_top


# food_info_cahe
def _save_foodinfo_into_foodcache(food_info) -> None:
    """запись компактной инфы о продукте из FS в файл food_cache"""

    temp_food_cache = {}
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

    # открываем сохраненные данные о продуктах из файла
    with open('fatsecret_app/food_info_cache.pickle', 'rb') as file:
        food_cache = pickle.load(file)
        food_cache.update(temp_food_cache)

    # записываем измененный кеш обратно в файл
    with open('fatsecret_app/food_info_cache.pickle', 'wb') as f:
        pickle.dump(food_cache, f)


def _get_foodinfo_from_foodcache(food_id:str):
    """добыча из кеша инфо о продукте в виде словаря:
    {'food_name': {данные для расчета нормального количества}}"""

    with open('fatsecret_app/food_info_cache.pickle', 'rb') as file:
        daily_total_cache = pickle.load(file)

    if daily_total_cache.get(food_id):
        food_info = daily_total_cache[food_id]
        print('food_info получена из кеша')
        return food_info

    return {}


def save_foodmetric_into_foodcache(prods_without_info) -> None:
    """получает словарь с продуктами, которым добавили метрику
    вручную в дневнике питания, и сохраняет в food_info_cache"""

    with open('fatsecret_app/food_info_cache.pickle', 'rb') as file:
        food_info_cache = pickle.load(file)

    count_of_prods = len(prods_without_info.get('food_id'))

    for i in range(count_of_prods):

        food_id = prods_without_info["food_id"][i]
        metric_serving_amount = prods_without_info["metric_serving_amount"][i]
        metric_serving_unit = prods_without_info["metric_serving_unit"][i]
        serving_id = prods_without_info["serving_id"][i]

        if type(food_info_cache[food_id]['servings']['serving']) is dict:
            food_info_cache[food_id]['servings']['serving']["metric_serving_amount"] = metric_serving_amount
            food_info_cache[food_id]['servings']['serving']["metric_serving_unit"] = metric_serving_unit
        else:
            for dic in food_info_cache[food_id]['servings']['serving']:
                if dic['serving_id'] == serving_id:
                    dic["metric_serving_amount"] = metric_serving_amount
                    dic["metric_serving_unit"] = metric_serving_unit
                    break
            
    with open('fatsecret_app/food_info_cache.pickle', 'wb') as f:
            pickle.dump(food_info_cache, f)   


# daily_total
def _create_daily_total(user, entry_date: datetime) -> dict:
    """возвращает словарь с суммарным количеством и калорийностью
    продуктов за один день в виде словаря:
    {'food_name': {'calories': ..., 'amount': ... , 'metric': ...},
     'food_name': {'calories': ..., 'amount': ... , 'metric': ...}}"""

    daily_total = {}
    without_info = {}
    daily_total_is_good = True

    fs_session = create_user_fs_session(user)
    daily_entries = fs_session.food_entries_get(date=entry_date)

    for food in daily_entries:

        # достаем подробную инфо о виде еды
        food_info = _get_foodinfo_from_foodcache(food['food_id'])
        food_info_found = True
        if not food_info:
            try:
                food_info = fs_session.food_get(food_id=food['food_id'])
                _save_foodinfo_into_foodcache(food_info)
            except FS_ParameterError:
                food_info_found = False
                food['cant_get_id'] = True
                daily_total_is_good = False

        if food_info_found:
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
                    # добавляем эту еду в спец.словарь и не считаем amount
                    without_info[food['food_id']] = {
                        'food_entry_name': food['food_entry_name'],
                        'serving_description': food['serving'].get('serving_description', 'порция'),
                        'serving_id': food['serving_id'],
                        'calories_per_serving': int(int(food['calories']) / float(food['number_of_units']))
                    }
                else:
                    # если в инфе метрика есть - считаем и добавляем к общему подсчету
                    food['norm_amount'] = int(float(food['number_of_units']) *
                                            float(food['serving']['metric_serving_amount']) *
                                            float(food['serving']['number_of_units']))  

        # меняем наименование на то, что в инфе, оно более общее
        if food_info_found:
            food['food_name'] = food_info['food_name']
        else:
            food['food_name'] = food['food_entry_name']
        # складываем у продуктов с одинаковым именем калории и вес
        if daily_total.get(food['food_name']) is None:
            daily_total[food['food_name']] = {'calories': 0, 'amount': 0}

        daily_total[food['food_name']]['calories'] += int(food['calories'])

        # если не получилось высчитать нормально количество - то продукт в списке without_info
        if food.get('norm_amount'):
            daily_total[food['food_name']]['amount'] += food['norm_amount']
            daily_total[food['food_name']]['metric'] = food['serving']['metric_serving_unit']

    if daily_total_is_good:
        _save_daily_total_in_cache(user, entry_date, daily_total)

    elif without_info:
        daily_total['without_info'] = without_info

    return daily_total

  
def _save_daily_total_in_cache(user, entry_date: datetime, daily_total:dict) -> None:
    """сохранение в кеше суммарного количества и калорий
    съеденной еды по названиям за один день для ускорения создания топов
    записываются даты старше 2 дней и единожды
    """

    # если есть without_info, не сохраняем
    if daily_total.get('without_info'):
        return

    # если прошло меньше 3 дней, не сохраняем
    entry_date = entry_date.date()
    if (date.today() - entry_date).days < 3:
        return 

    with open('fatsecret_app/daily_total_cache.pickle', 'rb') as file:
        daily_total_cache = pickle.load(file)

    if daily_total_cache.get(user.id):
        if daily_total_cache[user.id].get(entry_date):
            return
        else:
            daily_total_cache[user.id].update({entry_date:daily_total})
    else:
        daily_total_cache.update({user.id:{entry_date:daily_total}})

    with open('fatsecret_app/daily_total_cache.pickle', 'wb') as file:
        pickle.dump(daily_total_cache, file)


def _get_daily_total_from_cache(user, entry_date: datetime) -> dict:
    """добыча из кеша суммарного количества и калорий съеденной еды
    по названиям за один день в виде словаря:
    {'food_name': {'total_calories': ..., 'total_amount': ... , 'metric': ...}}"""

    entry_date = entry_date.date()

    with open('fatsecret_app/daily_total_cache.pickle', 'rb') as file:
        daily_total_cache = pickle.load(file)

    if daily_total_cache.get(user.id):
        if daily_total_cache[user.id].get(entry_date):
            daily_total = daily_total_cache[user.id][entry_date]
            print('daily_total получена из кеша')
            return daily_total

    return {}


# monthly_total
def _create_monthly_total(user, entry_month: datetime) -> dict:
    """возвращает словарь с суммарным количеством и калорийностью
    продуктов за один месяц в виде словаря, получая основу из FS:
    {'food_name': {'calories': ..., 'amount': ... , 'metric': ...},
     'food_name': {'calories': ..., 'amount': ... , 'metric': ...}}
    надо передать user и datetime"""

    monthly_total = {}

    fs_session = create_user_fs_session(user)
    monthly_entries = fs_session.food_entries_get_month(date=entry_month)

    # если словарь вместо списка, значит всего один день заполнен
    if type(monthly_entries) is dict:
        monthly_entries = [monthly_entries]

    # проходимся по каждому дню
    for day in monthly_entries:
        # узнаем его дату
        entry_month = epoch_into_datetime(int(day['date_int']))
        # добываем суммарности за день
        daily_total = _get_daily_total_from_cache(user, entry_month)
        if not daily_total:
            print('daily_total в кеше нет')
            daily_total = _create_daily_total(user, entry_month)
            _save_daily_total_in_cache(user, entry_month, daily_total)

        # суммируем в месячную сводку
        for key in daily_total.keys():
            if key == 'without_info':
                monthly_total['without_info'] = daily_total[key]
            elif monthly_total.get(key):
                monthly_total[key]['calories'] += daily_total[key]['calories']
                monthly_total[key]['amount'] += daily_total[key]['amount']
            else:
                monthly_total[key] = daily_total[key]

    if monthly_total:
         _save_monthly_total_in_cache(user, entry_month, monthly_total)

    return monthly_total


def _save_monthly_total_in_cache(user, entry_month: datetime, monthly_total:dict) -> None:
    """сохранение в кеше суммарного количества и калорий
    съеденной еды по названиям за один день для ускорения создания топов
    записываются даты старше 2 дней и единожды
    """

    # если есть without_info, не сохраняем
    if monthly_total.get('without_info'):
        return

    # если прошло меньше 3 дней, не сохраняем
    if (date.today() - entry_month.date()).days < 3:
        return 
    
    entry_month = entry_month.strftime("%Y-%m")
    current_month = date.today().strftime("%Y-%m")

    # если месяц - текущий, не сохраняем
    if entry_month == current_month:
        return

    with open('fatsecret_app/monthly_total_cache.pickle', 'rb') as file:
        monthly_total_cache = pickle.load(file)

    # если такого юзера еще не записано - сохраняем
    if monthly_total_cache.get(user.id) is None:

        monthly_total_cache.update({user.id:{entry_month:monthly_total}})

        with open('fatsecret_app/monthly_total_cache.pickle', 'wb') as file:
            pickle.dump(monthly_total_cache, file)

    # если такой юзер записан, но нет такого месяца - сохраняем
    if monthly_total_cache[user.id].get(entry_month) is None:

        monthly_total_cache[user.id].update({entry_month:monthly_total})

        with open('fatsecret_app/monthly_total_cache.pickle', 'wb') as file:
            pickle.dump(monthly_total_cache, file)


def _get_monthly_total_from_cache(user, entry_month: datetime) -> dict:
    """добыча из кеша суммарного количества и калорий съеденной еды
    по названиям за один месяц в виде словаря:
    {'food_name': {'total_calories': ..., 'total_amount': ... , 'metric': ...}}"""

    entry_month = entry_month.strftime("%Y-%m")

    with open('fatsecret_app/monthly_total_cache.pickle', 'rb') as file:
        monthly_total_cache = pickle.load(file)

    if monthly_total_cache.get(user.id):
        if monthly_total_cache[user.id].get(entry_month):
            monthly_total = monthly_total_cache[user.id][entry_month]
            print('monthly_total получена из кеша')
            return monthly_total

    return {}





def _clean_food_info_cache() -> None:
    """очистка файла кеша food_info_cache.pickle"""

    with open('fatsecret_app/food_info_cache.pickle', 'wb') as f:
        pickle.dump({}, f)


def _remove_prods_without_info_from_cache() -> None:
    """удаление записей о продуктах без метрики для тестов
    id '4652615' (184г) - твистер,  id '62258251' (135г) - картоха"""

    with open('fatsecret_app/food_info_cache.pickle', 'rb') as f:
        food_cache = pickle.load(f)

    #  твистер - (184г)
    if food_cache.get('4652615'):
        print(food_cache.get('4652615'))
        del food_cache['4652615']
    #  картоха - (135г)
    if food_cache.get('62258251'):
        print(food_cache.get('62258251'))
        del food_cache['62258251']

    with open('fatsecret_app/food_info_cache.pickle', 'wb') as f:
        pickle.dump(food_cache, f)


# _remove_prods_without_info_from_cache()

