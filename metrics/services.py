from datetime import date, datetime, timedelta

from home.utils import convert_date_to_epoch
from metrics.models import DailyData
from nutrition.decor import fs_error_catcher
from nutrition.managers import FSManager

fs = FSManager()


# TODO to metrics?
@fs_error_catcher
def renew_measure_nutrition(user, measure_date: datetime) -> None:
    """обновление кбжу в записи Measurements на данные из FS
    за выбранный день, если изменились калории"""

    if not fs.is_connected(user):
        return

    measure = DailyData.objects.filter(user=user, date=measure_date.date()).first()

    if measure:
        try:
            fs_nutrition = fs.daily_nutrition(user, measure_date)
        except KeyError:
            return

        if fs_nutrition:
            if fs_nutrition["calories"] != measure.calories:
                measure.calories = fs_nutrition["calories"]
                measure.protein = fs_nutrition["protein"]
                measure.fat = fs_nutrition["fat"]
                measure.carbohydrate = fs_nutrition["carbohydrate"]
                measure.save()


@fs_error_catcher
def renew_weekly_measures_nutrition(user) -> None:
    """обновление кбжу в записях DailyData за последние 7 дней
    на данные из FS, но если изменились калории"""

    if not fs.is_connected(user):
        return

    weekly_nutrition_fs = fs.weekly_nutrition(user)

    if not weekly_nutrition_fs:
        return

    for i in range(7):
        measure_date = date.today() - timedelta(days=(6 - i))
        measure = DailyData.objects.filter(user=user, date=measure_date).first()

        if measure:
            measure_date_int = convert_date_to_epoch(measure.date)
            if weekly_nutrition_fs.get(measure_date_int):
                if measure.calories != weekly_nutrition_fs[measure_date_int]["calories"]:
                    measure.calories = weekly_nutrition_fs[measure_date_int]["calories"]
                    measure.protein = weekly_nutrition_fs[measure_date_int]["protein"]
                    measure.fat = weekly_nutrition_fs[measure_date_int]["fat"]
                    measure.carbohydrate = weekly_nutrition_fs[measure_date_int][
                        "carbohydrate"
                    ]
                    measure.save()
