from .models import Measurement, MeasureIndex, MeasureColor, MeasureColorField
from .forms import MeasurementForm, MeasurementCommentForm
from datetime import date, timedelta
from typing import Union
from fatsecret_app.services import *


def get_daily_measure(user, measure_date:date=None):
    """возвращает измерения за день, по умолчанию - за сегодня"""

    if measure_date is None:
        measure_date = date.today()
        
    measure = Measurement.objects.filter(
        date__exact=measure_date, user=user).first()

    return measure


def get_last_measures(user, days:int=7):
    """возвращает последние измерения, по умолчанию за 7 дней"""

    measures = Measurement.objects.filter(user=user)[:days]

    return measures


def get_measure_comment_forms(measurements_set):
    """возвращает список форм для комментариев к измерениям 
    для переданного QuerySet модели Measurements"""

    measure_comment_forms = []
    for day in reversed(measurements_set):
        comment_form = MeasurementCommentForm(instance=day)
        measure_comment_forms.append(comment_form)

    return measure_comment_forms


def user_has_measeurecolor_settings(user) -> bool:
    """проверяет, настроены ли у пользователя окрашивания 
    физических показателей экспертом"""

    result = bool(MeasureColorField.objects.filter(user_id=user))

    return result


def get_measeurecolor_settings(user):
    """возвращает настройки окрашивания показателей клиента в виде Queryset"""

    if user_has_measeurecolor_settings(user):
        colorsettings = MeasureColorField.objects.filter(user=user)
        colorsettings.order_by('index', 'color')
    else:
        return None

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
    for object in colorsettings:
        data[str(object.index)][str(object.color.id)] = {
                                'color': str(object.color),
                                'low': str(object.low_limit),
                                'up': str(object.upper_limit) }

    return data


def create_weekly_measure_forms(user):
    """создает список форм для измерений на последние семь дней"""

    weekly_measure_forms = []

    for i in range(7):
        measure_date = date.today() - timedelta(days=i)
        measure = Measurement.objects.filter(date=measure_date, user=user).first()

        if not measure:
            measure_form = MeasurementForm()
            # в нее сразу записывается user и дата
            measure_form = measure_form.save(commit=False)
            measure_form.user = user
            measure_form.date = measure_date
            # сохраняется запись в базе
            measure_form.save()

            # готовая форма на основе сущеcтсвующей пустой записи БД
            measure = Measurement.objects.get(date=measure_date, user=user)

        measure_form = MeasurementForm(instance=measure)

        weekly_measure_forms.append(measure_form)

    return weekly_measure_forms


def renew_measure_nutrition(user, measure_date:datetime) -> None:
    """обновление кбжу в записи Measurements на данные из FS
    за выбранный день, если изменились калории"""

    measure = Measurement.objects.filter(user=user, date=measure_date.date()).first()

    if user_has_fs_entry(user) and measure:
        fs_nutrition = get_daily_nutrition_fs(user, measure_date)

        if fs_nutrition:
            if fs_nutrition['calories'] != measure.calories:
                measure.calories = fs_nutrition['calories']
                measure.protein = fs_nutrition['protein']
                measure.fats = fs_nutrition['fat']
                measure.carbohydrates = fs_nutrition['carbohydrate']
                measure.save()


def renew_weekly_measures_nutrition(user) -> None:
    """обновление кбжу в записях Measurements за последние 7 дней
    на данные из FS, но если изменились калории"""

    weekly_nutrition_fs = get_weekly_nutrition_fs(user)

    for i in range(7):
        measure_date = date.today() - timedelta(days=(6-i))
        measure = Measurement.objects.filter(user=user, date=measure_date).first()

        if measure:
            measure_date_int = _date_into_epoch(measure.date)
            if weekly_nutrition_fs.get(measure_date_int):
                if (measure.calories !=
                    weekly_nutrition_fs[measure_date_int]['calories']):
                    measure.calories = weekly_nutrition_fs[measure_date_int]['calories']
                    measure.protein = weekly_nutrition_fs[measure_date_int]['protein']
                    measure.fats = weekly_nutrition_fs[measure_date_int]['fat']
                    measure.carbohydrates = weekly_nutrition_fs[measure_date_int]['carbohydrate']
                    measure.save()


def _epoch_into_date(date_epoch: int) -> date:
    """конвертирует число дней с 1970 в date"""

    date_date = date(1970, 1, 1) + timedelta(days=date_epoch)

    return date_date


def _date_into_epoch(request_date: date) -> int:
    """превращает datetime в число дней с 1970"""

    date_int = str((request_date - date(1970, 1, 1)).days)

    return date_int
