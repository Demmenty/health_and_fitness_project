from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Union

from django.conf import settings
from fatsecret import (
    Fatsecret as FS,
    ParameterError as FS_ParameterError,
)

from common.cache_manager import cache
from common.utils import datetime_into_epoch, epoch_into_datetime

from .decor import fs_error_catcher
from .models import FatSecretEntry

CURRENT_DIR = Path(__file__).resolve().parent


class FatsecretManager:
    """функции для работы с FS"""

    def __init__(self):
        self.session = FS(
            settings.FS_CONSUMER_KEY, settings.FS_CONSUMER_SECRET
        )

    def client_session(self, user):
        """возвращает сессию для взаимодействия с FatSecret
        для конкретного пользователя"""

        userdata = FatSecretEntry.objects.get(user=user)
        session_token = (userdata.oauth_token, userdata.oauth_token_secret)
        session = FS(
            settings.FS_CONSUMER_KEY,
            settings.FS_CONSUMER_SECRET,
            session_token=session_token,
        )
        return session

    def save_token(self, session_token, user) -> None:
        """сохранение токена для взаимодействия с FS в базе данных"""

        FatSecretEntry.objects.update_or_create(
            user=user,
            defaults={
                "oauth_token": session_token[0],
                "oauth_token_secret": session_token[1],
            },
        )

    def is_connected(self, user) -> bool:
        """Проверяет, привязан ли у пользователя аккаунт Fatsecret"""

        return FatSecretEntry.objects.filter(user=user).exists()

    @fs_error_catcher
    def send_weight(
        self, user, measure_weight: str, measure_date: date
    ) -> None:
        """отправка показателя веса клиента в аккаунт приложения fatsecret.
        вес записывается, только, если еще нет записи за этот день или свежее
        """

        session = self.client_session(user)

        measure_weight = float(measure_weight)
        measure_datetime = datetime.combine(measure_date, time())
        measure_date_int = datetime_into_epoch(measure_datetime)

        try:
            # проверяем существующие внесения веса в fatsecret
            monthly_weights = session.weights_get_month()
        except KeyError as error:
            print("Возникла KeyError при отправке веса в FatSecret!", error)

            session.weight_update(
                current_weight_kg=measure_weight, date=measure_datetime
            )
            return

        if monthly_weights:
            if type(monthly_weights) is dict:
                last_record_date_int = monthly_weights["date_int"]
            else:
                last_record_date_int = monthly_weights[-1]["date_int"]

            if last_record_date_int < measure_date_int:
                session.weight_update(
                    current_weight_kg=measure_weight, date=measure_datetime
                )
        else:
            session.weight_update(
                current_weight_kg=measure_weight, date=measure_datetime
            )

    def daily_nutrition(
        self, user, request_date: datetime
    ) -> Union[dict, None]:
        """получение словаря с кбжу из FS за запрошенный день"""

        session = self.client_session(user)

        monthly_nutrition = session.food_entries_get_month(date=request_date)

        if not monthly_nutrition:
            return {}

        if type(monthly_nutrition) is dict:
            monthly_nutrition = [monthly_nutrition]

        for day in monthly_nutrition:
            if day["date_int"] == datetime_into_epoch(request_date):
                return day

    def weekly_nutrition(self, user) -> dict:
        """получение словаря с кбжу из FS за последние 7 дней
        ключи словаря - date_int:str"""

        session = self.client_session(user)

        week_nutrition_list = []

        # получаем данные по текущему месяцу
        try:
            current_month_nutrition = session.food_entries_get_month()
        except KeyError:
            return {}

        if type(current_month_nutrition) is dict:
            week_nutrition_list += [current_month_nutrition]
        else:
            week_nutrition_list += current_month_nutrition

        # если сегодня 6 число или меньше, добавить и предыдущий месяц
        if date.today().day < 7:
            try:
                previous_month_nutrition = session.food_entries_get_month(
                    date=datetime.today() - timedelta(weeks=4)
                )
                if type(previous_month_nutrition) is dict:
                    week_nutrition_list += [previous_month_nutrition]
                else:
                    week_nutrition_list += previous_month_nutrition
            except KeyError:
                ...

        # фильтруем новейшие 7 записей
        week_nutrition_list = sorted(
            week_nutrition_list, key=lambda x: x["date_int"], reverse=True
        )[:7]

        # превращаем в словарь с ключами = date_int
        week_nutrition_dic = {}
        for day in week_nutrition_list:
            week_nutrition_dic[day["date_int"]] = day
            del week_nutrition_dic[day["date_int"]]["date_int"]

        return week_nutrition_dic

    def daily_food(self, user, request_date: datetime) -> dict:
        """Подсчитывает данные о съеденных продуктах за день"""

        session = self.client_session(user)

        daily_entries = session.food_entries_get(date=request_date)
        if not daily_entries:
            return {}
        
        result = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Other": [],
            "without_metric": {},
            "total": {
                "amount": 0,
                "nutrition": {
                    "calories": 0,
                    "protein": 0,
                    "fat": 0,
                    "carbohydrate": 0,
                }
            }
        }

        # складываем одинаковую еду в этот словарик (для топов)
        daily_total = {}
        # для понимания, можно сохранить итог, или нет
        daily_total_ok_for_save = True

        # обработка каждой записи о продукте
        for food in daily_entries:
            # поиск подробностей о продукте для подсчета порции
            food_info = cache.fs.get_foodinfo(food["food_id"])
            food_info_found = True
            if not food_info:
                try:
                    food_info = session.food_get(food_id=food["food_id"])
                    cache.fs.save_foodinfo(food_info)
                except FS_ParameterError:
                    food_info_found = False
                    food["cant_get_id"] = True
                    daily_total_ok_for_save = False

            if food_info_found:
                # добавление инфы в food для соответствующего вида порции
                if type(food_info["servings"]["serving"]) is list:
                    for serv_info in food_info["servings"]["serving"]:
                        if serv_info["serving_id"] == food["serving_id"]:
                            food["serving"] = serv_info
                            break
                else:
                    food["serving"] = food_info["servings"]["serving"]

                # добавляем нормальное отображение количества
                # если измерение в г или мл - считаем как есть
                if (
                    food["serving"]["measurement_description"] == "g"
                    or food["serving"]["measurement_description"] == "ml"
                ):
                    food["norm_amount"] = int(float(food["number_of_units"]))
                    result["total"]["amount"] += food["norm_amount"]
                else:
                    # если измерение в порциях - сначала проверяем, есть ли граммовка порции
                    if food["serving"].get("metric_serving_amount") is None:
                        # если в инфе не оказалось граммовки порции
                        # добавляем эту еду в спец.словарь и не считаем amount
                        daily_total_ok_for_save = False
                        result["without_metric"][food["food_id"]] = {
                            "food_entry_name": food["food_entry_name"],
                            "serving_description": food["serving"].get(
                                "serving_description", "порция"
                            ),
                            "serving_id": food["serving_id"],
                            "calories_per_serving": int(
                                int(food["calories"])
                                / float(food["number_of_units"])
                            ),
                        }
                    else:
                        # если в инфе метрика есть - считаем и добавляем к общему подсчету
                        food["norm_amount"] = int(
                            float(food["number_of_units"])
                            * float(food["serving"]["metric_serving_amount"])
                            * float(food["serving"]["number_of_units"])
                        )
                        result["total"]["amount"] += food["norm_amount"]

            # отфильтровать ненужное и добавить в результат
            if food.get('serving'):
                if food["serving"].get("metric_serving_unit"):
                    food["metric_serving_unit"] = food["serving"]["metric_serving_unit"]
                del food["serving"]
            del food["date_int"]
            del food["food_entry_description"]
            del food["food_entry_id"]
            del food["serving_id"]
            del food["food_id"]
            result[food["meal"]].append(food)
            # подсчет итоговой суммы кбжу
            result["total"]["nutrition"]["calories"] += int(food["calories"])
            result["total"]["nutrition"]["protein"] += float(food["protein"])
            result["total"]["nutrition"]["fat"] += float(food["fat"])
            result["total"]["nutrition"]["carbohydrate"] += float(food["carbohydrate"])

            # заодно готовим daily_total
            # меняем наименование на то, что в инфе, оно более общее
            if food_info_found:
                food["food_name"] = food_info["food_name"]
            else:
                food["food_name"] = food["food_entry_name"]
            # складываем у продуктов с одинаковым именем калории и вес
            if daily_total.get(food["food_name"]) is None:
                daily_total[food["food_name"]] = {
                    "calories": 0,
                    "amount": 0,
                }
            daily_total[food["food_name"]]["calories"] += int(food["calories"])
            # если получилось высчитать нормально количество
            # (если нет - то продукт в списке without_metric, либо не имеет такого ключа)
            if food.get("norm_amount"):
                daily_total[food["food_name"]]["amount"] += food["norm_amount"]
                daily_total[food["food_name"]]["metric"] = food["metric_serving_unit"]

        # округляем результаты в получившемся итоге по кбжу
        for key, value in result["total"]["nutrition"].items():
            result["total"]["nutrition"][key] = round(value, 2)

        # сохраняем daily_total в кеше на будущее для топов
        if daily_total_ok_for_save:
            cache.fs.save_daily_total(user, request_date, daily_total)

        return result
    

    def monthly_food(self, user, request_date) -> dict:
        """Подсчитывает данные о съеденных продуктах за месяц"""

        session = self.client_session(user)

        try:
            monthly_entries = session.food_entries_get_month(date=request_date)
        except KeyError:
            return {}
        if not monthly_entries:
            return {}
        
        result = {
            "days": [],
            "avg": {},
        }

        if type(monthly_entries) is dict:
            days_count = 1
        else:
            days_count = len(monthly_entries)
        
        if days_count == 1:
            monthly_entries["date"] = date_int_to_date(monthly_entries["date_int"])
            del monthly_entries["date_int"]
            result["days"].append(monthly_entries)

            if monthly_entries["date"] == date.today():
                result["avg"] = {
                    "protein": "-", 
                    "fat": "-", 
                    "carbohydrate": "-", 
                    "calories": "-"
                }
            else:
                result["avg"] = {
                    "protein": monthly_entries["protein"], 
                    "fat": monthly_entries["fat"], 
                    "carbohydrate": monthly_entries["carbohydrate"], 
                    "calories": monthly_entries["calories"],
                }
        
        if days_count > 1:
            result["avg"] = {"protein": 0, "fat": 0, "carbohydrate": 0, "calories": 0}

            for day in monthly_entries:
                day["date"] = date_int_to_date(day["date_int"])
                del day["date_int"]
                result["days"].append(day)

                if day["date"] == date.today():
                    days_count -= 1
                    break

                result["avg"]["protein"] += float(day["protein"])
                result["avg"]["fat"] += float(day["fat"])
                result["avg"]["carbohydrate"] += float(day["carbohydrate"])
                result["avg"]["calories"] += float(day["calories"])

            result["avg"]["protein"] = round(result["avg"]["protein"] / days_count, 2)
            result["avg"]["fat"] = round(result["avg"]["fat"] / days_count, 2)
            result["avg"]["carbohydrate"] = round(result["avg"]["carbohydrate"] / days_count, 2)
            result["avg"]["calories"] = round(result["avg"]["calories"] / days_count, 2)

        return result
    

    def daily_total(self, user, entry_date: datetime) -> dict:
        """возвращает словарь с суммарным количеством и калорийностью
        продуктов за один день в виде словаря:
        {'food_name': {'calories': ..., 'amount': ... , 'metric': ...},
        'food_name': {'calories': ..., 'amount': ... , 'metric': ...}}"""

        daily_total = {}
        without_metric= {}
        daily_total_ok_for_save = True

        session = self.client_session(user)
        daily_entries = session.food_entries_get(date=entry_date)

        for food in daily_entries:
            # достаем подробную инфо о виде еды
            food_info = cache.fs.get_foodinfo(food["food_id"])
            food_info_found = True
            if not food_info:
                try:
                    food_info = session.food_get(food_id=food["food_id"])
                    cache.fs.save_foodinfo(food_info)
                except FS_ParameterError:
                    food_info_found = False
                    food["cant_get_id"] = True
                    daily_total_ok_for_save = False

            if food_info_found:
                # добавление инфы в food для соответствующего вида порции
                if type(food_info["servings"]["serving"]) is list:
                    for serv_info in food_info["servings"]["serving"]:
                        if serv_info["serving_id"] == food["serving_id"]:
                            food["serving"] = serv_info
                            break
                else:
                    food["serving"] = food_info["servings"]["serving"]

                # добавляем нормальное отображение количества
                # если измерение в г или мл - считаем как есть
                if (
                    food["serving"]["measurement_description"] == "g"
                    or food["serving"]["measurement_description"] == "ml"
                ):
                    food["norm_amount"] = int(float(food["number_of_units"]))
                else:
                    # если измерение в порциях - сначала проверяем, есть ли граммовка порции
                    if food["serving"].get("metric_serving_amount") is None:
                        daily_total_ok_for_save = False
                        # если в инфе не оказалось граммовки порции
                        # добавляем эту еду в спец.словарь и не считаем amount
                        without_metric[food["food_id"]] = {
                            "food_entry_name": food["food_entry_name"],
                            "serving_description": food["serving"].get(
                                "serving_description", "порция"
                            ),
                            "serving_id": food["serving_id"],
                            "calories_per_serving": int(
                                int(food["calories"])
                                / float(food["number_of_units"])
                            ),
                        }
                    else:
                        # если в инфе метрика есть - считаем и добавляем к общему подсчету
                        food["norm_amount"] = int(
                            float(food["number_of_units"])
                            * float(food["serving"]["metric_serving_amount"])
                            * float(food["serving"]["number_of_units"])
                        )

            # меняем наименование на то, что в инфе, оно более общее
            if food_info_found:
                food["food_name"] = food_info["food_name"]
            else:
                food["food_name"] = food["food_entry_name"]
            # складываем у продуктов с одинаковым именем калории и вес
            if daily_total.get(food["food_name"]) is None:
                daily_total[food["food_name"]] = {"calories": 0, "amount": 0}

            daily_total[food["food_name"]]["calories"] += int(food["calories"])

            # если не получилось высчитать нормально количество - то продукт в списке without_metric
            if food.get("norm_amount"):
                daily_total[food["food_name"]]["amount"] += food["norm_amount"]
                daily_total[food["food_name"]]["metric"] = food["serving"][
                    "metric_serving_unit"
                ]

        if daily_total_ok_for_save:
            cache.fs.save_daily_total(user, entry_date, daily_total)

        elif without_metric:
            daily_total["without_metric"] = without_metric

        return daily_total

    def monthly_total(self, user, entry_month: datetime) -> dict:
        """возвращает словарь с суммарным количеством и калорийностью
        продуктов за один месяц в виде словаря, получая основу из FS:
        {'food_name': {'calories': ..., 'amount': ... , 'metric': ...},
        'food_name': {'calories': ..., 'amount': ... , 'metric': ...}}
        надо передать user и datetime"""

        monthly_total = {}

        session = self.client_session(user)

        try:
            monthly_entries = session.food_entries_get_month(date=entry_month)
        except KeyError:
            return {}

        # если словарь вместо списка, значит всего один день заполнен
        if type(monthly_entries) is dict:
            monthly_entries = [monthly_entries]

        # проходимся по каждому дню
        for day in monthly_entries:
            # узнаем его дату
            entry_month = epoch_into_datetime(int(day["date_int"]))
            # добываем суммарности за день
            daily_total = cache.fs.get_daily_total(user, entry_month)
            if not daily_total:
                daily_total = self.daily_total(user, entry_month)
                cache.fs.save_daily_total(user, entry_month, daily_total)

            # суммируем в месячную сводку
            for key in daily_total.keys():
                if key == "without_metric":
                    monthly_total["without_metric"] = daily_total[key]
                elif monthly_total.get(key):
                    monthly_total[key]["calories"] += daily_total[key][
                        "calories"
                    ]
                    monthly_total[key]["amount"] += daily_total[key]["amount"]
                else:
                    monthly_total[key] = daily_total[key]

        if monthly_total:
            cache.fs.save_monthly_total(user, entry_month, monthly_total)

        return monthly_total

    def daily_top(self, user, entry_date: datetime) -> dict:
        """создание топ-3 продуктов за месяц, по весу и по калориям"""

        daily_total = cache.fs.get_daily_total(user, entry_date)

        if not daily_total:
            daily_total = self.daily_total(user, entry_date)
            cache.fs.save_daily_total(user, entry_date, daily_total)

        daily_top = {}

        if daily_total.get("without_metric"):
            daily_top["without_metric"] = daily_total["without_metric"]
            del daily_total["without_metric"]

        top_calories = dict(
            sorted(
                daily_total.items(),
                key=lambda x: x[1]["calories"],
                reverse=True,
            )[:3]
        )

        top_amount = dict(
            sorted(
                daily_total.items(), key=lambda x: x[1]["amount"], reverse=True
            )[:3]
        )

        daily_top.update(
            {"top_calories": top_calories, "top_amount": top_amount}
        )

        return daily_top

    def monthly_top(self, user_id, month: datetime) -> dict:
        """создание топ-10 продуктов за месяц, по весу и по калориям"""

        monthly_total = cache.fs.get_monthly_total(user_id, month)

        if not monthly_total:
            monthly_total = self.monthly_total(user_id, month)

            if monthly_total.get("without_metric") is None:
                cache.fs.save_monthly_total(user_id, month, monthly_total)

        result = {
            "without_metric": [],
            "calories": {},
            "amount": {},
        }

        if monthly_total.get("without_metric"):
            result["without_metric"] = monthly_total["without_metric"]
            del monthly_total["without_metric"]

        result["calories"] = dict(
            sorted(
                monthly_total.items(),
                key=lambda x: x[1]["calories"],
                reverse=True,
            )[:10]
        )
        result["amount"] = dict(
            sorted(
                monthly_total.items(),
                key=lambda x: x[1]["amount"],
                reverse=True,
            )[:10]
        )
        return result


def date_int_to_date(date_int:int) -> datetime.date:
    """Возвращает время в формате date YYYY-MM-DD"""

    result = date(1970, 1, 1) + timedelta(days=int(date_int))
    return result
