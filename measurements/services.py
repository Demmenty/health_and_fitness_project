from datetime import date, timedelta

from common.services import services
from common.utils import date_into_epoch
from fatsecret_app.decor import fs_error_catcher
from fatsecret_app.services import *

from .forms import (
    MeasureColorFieldForm,
    MeasurementCommentForm,
    MeasurementForm,
)
from .models import MeasureColorField, Measurement


# measures
def get_daily_measure(user, measure_date: date = None):
    """возвращает измерения за день, по умолчанию - за сегодня"""

    if measure_date is None:
        measure_date = date.today()

    measure = Measurement.objects.filter(
        date__exact=measure_date, user=user
    ).first()

    return measure


def get_last_measures(user, days: int = 7):
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


def create_weekly_measure_forms(user):
    """создает список форм для измерений на последние семь дней
    если запись отсутствует - создает пустую
    """

    weekly_measure_forms = []

    for i in range(7):
        measure_date = date.today() - timedelta(days=i)
        measure = Measurement.objects.filter(
            date=measure_date, user=user
        ).first()

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


def create_avg_for_measures(period_measures) -> dict:
    """Составляет словарь из средних значений по
    каждому ежедневному измерению физических показателей
    Нужно передать QuerySet измерений Measurements
    """

    period_measures = list(period_measures.values())

    avg_data = {}

    if any(day["feel"] for day in period_measures):
        days = 0
        feel_total = 0
        for day in period_measures:
            if day["feel"]:
                feel_total += int(day["feel"])
                days += 1
        avg = round(feel_total / days)
        avg_data["feel"] = str(avg) + "/10"

    if any(day["weight"] for day in period_measures):
        days = 0
        weight_total = 0
        for day in period_measures:
            if day["weight"]:
                weight_total += float(day["weight"])
                days += 1
        avg = round(weight_total / days, 1)
        avg_data["weight"] = str(avg) + " кг"

    if any(day["fat"] for day in period_measures):
        days = 0
        fat_total = 0
        for day in period_measures:
            if day["fat"]:
                fat_total += float(day["fat"])
                days += 1
        avg = round(fat_total / days, 1)
        avg_data["fat"] = str(avg) + " %"

    if any(day["pulse"] for day in period_measures):
        days = 0
        pulse_total = 0
        for day in period_measures:
            if day["pulse"]:
                pulse_total += int(day["pulse"])
                days += 1
        avg = int(pulse_total / days)
        avg_data["pulse"] = avg

    if any(
        day["pressure_upper"] and day["pressure_lower"]
        for day in period_measures
    ):
        days = 0
        pressure_upper = 0
        pressure_lower = 0
        for day in period_measures:
            if day["pressure_upper"] and day["pressure_lower"]:
                pressure_upper += int(day["pressure_upper"])
                pressure_lower += int(day["pressure_lower"])
                days += 1
        avg_data["pressure"] = (
            str(int(pressure_upper / days))
            + "/"
            + str(int(pressure_lower / days))
        )

    # КБЖУ считается без учета сегодняшнего дня
    for i in range(len(period_measures)):
        if period_measures[i]["date"] == date.today():
            del period_measures[i]
            break

    # если calories none или 0 - нет смысла считать кбжу
    if any(day["calories"] for day in period_measures):
        days = 0
        calories_total = 0
        protein_total = 0
        fats_total = 0
        carbohydrates_total = 0

        for day in period_measures:
            if day["calories"]:
                days += 1
                calories_total += int(day["calories"])
            if day["protein"] is not None:
                protein_total += float(day["protein"])
            if day["fats"] is not None:
                fats_total += float(day["fats"])
            if day["carbohydrates"] is not None:
                carbohydrates_total += float(day["carbohydrates"])

        avg = int(calories_total / days)
        avg_data["calories"] = str(avg)

        avg = int(protein_total / days)
        avg_data["protein"] = str(avg)

        avg = int(fats_total / days)
        avg_data["fats"] = str(avg)

        avg = int(carbohydrates_total / days)
        avg_data["carbohydrates"] = str(avg)

    return avg_data


# measeurecolors
def user_has_measeurecolor_settings(user) -> bool:
    """проверяет, настроены ли у пользователя окрашивания
    физических показателей экспертом"""

    result = bool(MeasureColorField.objects.filter(user_id=user))

    return result


def get_measurecolor_settings(user):
    """возвращает настройки окрашивания показателей клиента в виде Queryset"""

    if user_has_measeurecolor_settings(user):
        instance = MeasureColorField.objects.filter(user=user)
        instance.order_by("index", "color")
    else:
        return {}

    colorsettings = {
        "feel": {},
        "weight": {},
        "fat": {},
        "pulse": {},
        "pressure_upper": {},
        "pressure_lower": {},
        "calories": {},
        "protein": {},
        "fats": {},
        "carbohydrates": {},
    }

    for object in instance:
        colorsettings[str(object.index)][str(object.color.id)] = {
            "color": str(object.color.color),
            "low": str(object.low_limit),
            "up": str(object.upper_limit),
        }

    return colorsettings


def save_measeurecolor_settings(user, colorset_values) -> None:
    """сохраняет окрашивания физических показателей от эксперта в БД"""

    if user_has_measeurecolor_settings(user):
        for index, color, low, up in colorset_values:
            if not low:
                low = None
            if not up:
                up = None
            instance = MeasureColorField.objects.filter(
                user=user, index_id=index, color_id=color
            )
            instance.update(low_limit=low, upper_limit=up)
    else:
        for index, color, low, up in colorset_values:
            if not low:
                low = None
            if not up:
                up = None
            MeasureColorField.objects.create(
                user=user,
                index_id=index,
                color_id=color,
                low_limit=low,
                upper_limit=up,
            )


def create_colorset_forms(client) -> list:
    """создает формы для того, что эксперт настроил окрашивания
    показателей в соответствующие цвета"""

    colorset_forms = []

    if user_has_measeurecolor_settings(client):
        for index_id in range(1, 11):
            for color_id in range(2, 7):
                instance = MeasureColorField.objects.get(
                    user=client, index_id=index_id, color_id=color_id
                )
                form = MeasureColorFieldForm(instance=instance)
                colorset_forms.append(form)
    else:
        for index_id in range(1, 11):
            for color_id in range(2, 7):
                form = MeasureColorFieldForm(
                    initial={
                        "user": client,
                        "index": index_id,
                        "color": color_id,
                    }
                )
                colorset_forms.append(form)

    return colorset_forms


@fs_error_catcher
def renew_measure_nutrition(user, measure_date: datetime) -> None:
    """обновление кбжу в записи Measurements на данные из FS
    за выбранный день, если изменились калории"""

    if not services.fs.is_connected(user):
        return

    measure = Measurement.objects.filter(
        user=user, date=measure_date.date()
    ).first()

    if measure:
        try:
            fs_nutrition = services.fs.daily_nutrition(user, measure_date)
        except KeyError:
            return

        if fs_nutrition:
            if fs_nutrition["calories"] != measure.calories:
                measure.calories = fs_nutrition["calories"]
                measure.protein = fs_nutrition["protein"]
                measure.fats = fs_nutrition["fat"]
                measure.carbohydrates = fs_nutrition["carbohydrate"]
                measure.save()


@fs_error_catcher
def renew_weekly_measures_nutrition(user) -> None:
    """обновление кбжу в записях Measurements за последние 7 дней
    на данные из FS, но если изменились калории"""

    if not services.fs.is_connected(user):
        return

    weekly_nutrition_fs = services.fs.weekly_nutrition(user)

    if not weekly_nutrition_fs:
        return

    for i in range(7):
        measure_date = date.today() - timedelta(days=(6 - i))
        measure = Measurement.objects.filter(
            user=user, date=measure_date
        ).first()

        if measure:
            measure_date_int = date_into_epoch(measure.date)
            if weekly_nutrition_fs.get(measure_date_int):
                if (
                    measure.calories
                    != weekly_nutrition_fs[measure_date_int]["calories"]
                ):
                    measure.calories = weekly_nutrition_fs[measure_date_int][
                        "calories"
                    ]
                    measure.protein = weekly_nutrition_fs[measure_date_int][
                        "protein"
                    ]
                    measure.fats = weekly_nutrition_fs[measure_date_int]["fat"]
                    measure.carbohydrates = weekly_nutrition_fs[
                        measure_date_int
                    ]["carbohydrate"]
                    measure.save()
