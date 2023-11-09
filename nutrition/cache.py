import os
import pickle
from datetime import date, datetime
from pathlib import Path
from typing import Union

CURRENT_DIR = Path(__file__).resolve().parent

# TODO REDO


class FatsecretCacheManager:
    """менеджер по работе с кешем fatsecret"""

    def __init__(self):
        self.servings = str(CURRENT_DIR) + "/cache/servings.pickle"
        self.daily_total_cache = (
            str(CURRENT_DIR) + "/cache/daily_total_cache.pickle"
        )
        self.monthly_total_cache = (
            str(CURRENT_DIR) + "/cache/monthly_total_cache.pickle"
        )

        if not self._caches_exist():
            self._create_caches()

    def _caches_exist(self) -> bool:
        """проверяет, существуют ли кеши"""

        if (
            Path.exists(CURRENT_DIR / "cache" / "servings.pickle")
            and Path.exists(CURRENT_DIR / "cache" / "daily_total_cache.pickle")
            and Path.exists(
                CURRENT_DIR / "cache" / "monthly_total_cache.pickle"
            )
        ):
            return True
        else:
            return False

    def _create_caches(self) -> None:
        """создает файлы для хранения кеша"""

        if not Path.exists(CURRENT_DIR / "cache"):
            os.makedirs(CURRENT_DIR / "cache")

        with open(self.servings, "wb") as f:
            pickle.dump({}, f)
        with open(self.daily_total_cache, "wb") as f:
            pickle.dump({}, f)
        with open(self.monthly_total_cache, "wb") as f:
            pickle.dump({}, f)

    def get_servings(self, food_id: str) -> Union[dict, None]:
        """добыча из кеша инфо о продукте по food_id в виде словаря:
        {'food_name': {данные для расчета нормального количества}}"""

        with open(self.servings, "rb") as file:
            cache = pickle.load(file)

        if cache.get(food_id):
            food_info = cache[food_id]
            return food_info
        else:
            return {}

    def save_servings(self, food_info) -> None:
        """запись компактной инфы о продукте из FS в файл food_cache"""

        temp_cache = {}
        # обработка для компактного сохранения
        if type(food_info["servings"]["serving"]) is dict:
            temp_cache[food_info["food_id"]] = {
                "food_name": food_info["food_name"],
                "servings": {
                    "serving": {
                        "serving_id": food_info["servings"]["serving"][
                            "serving_id"
                        ],
                        "measurement_description": food_info["servings"][
                            "serving"
                        ]["measurement_description"],
                        "metric_serving_amount": food_info["servings"][
                            "serving"
                        ].get("metric_serving_amount", None),
                        "number_of_units": food_info["servings"]["serving"][
                            "number_of_units"
                        ],
                        "metric_serving_unit": food_info["servings"][
                            "serving"
                        ].get("metric_serving_unit", None),
                        "serving_description": food_info["servings"][
                            "serving"
                        ]["serving_description"],
                    }
                },
            }
        else:
            temp_cache[food_info["food_id"]] = {
                "food_name": food_info["food_name"],
                "servings": {"serving": []},
            }
            for dic in food_info["servings"]["serving"]:
                temp_cache[food_info["food_id"]]["servings"]["serving"].append(
                    {
                        "serving_id": dic["serving_id"],
                        "measurement_description": dic[
                            "measurement_description"
                        ],
                        "metric_serving_amount": dic.get(
                            "metric_serving_amount", None
                        ),
                        "number_of_units": dic["number_of_units"],
                        "metric_serving_unit": dic.get(
                            "metric_serving_unit", None
                        ),
                        "serving_description": dic["serving_description"],
                    }
                )

        # открываем сохраненные данные о продуктах из файла
        with open(self.servings, "rb") as file:
            cache = pickle.load(file)
            cache.update(temp_cache)

        # записываем измененный кеш обратно в файл
        with open(self.servings, "wb") as f:
            pickle.dump(cache, f)

    def _remove_prods_no_metric(self) -> None:
        """удаление записей о продуктах без метрики для тестов
        id '4652615' (184г) - твистер,  id '62258251' (135г) - картоха"""

        with open(self.servings, "rb") as f:
            cache = pickle.load(f)

        #  твистер - (184г)
        if cache.get("4652615"):
            del cache["4652615"]
        #  картоха - (135г)
        if cache.get("62258251"):
            del cache["62258251"]

        with open(self.servings, "wb") as f:
            pickle.dump(cache, f)

    def save_serving(self, servings: dict) -> None:
        """
        Saves the servings provided in the `servings` parameter to the cache file.
        
        Args:
            servings (dict): A dictionary containing the servings to be saved. 
            The dictionary should have the following keys:
                - "food_id" (list): A list of food IDs.
                - "serving_id" (list): A list of serving IDs.
                - "metric_serving_amount" (list): A list of metric serving amounts.
                - "metric_serving_unit" (list): A list of metric serving units.
        """

        with open(self.servings, "rb") as file:
            cache: dict = pickle.load(file)

        amount_of_food = len(servings.get("food_id"))

        for i in range(amount_of_food):
            food_id = servings["food_id"][i]

            new_serving = {
                "serving_id": servings["serving_id"][i],
                "metric_serving_amount": servings["metric_serving_amount"][i],
                "metric_serving_unit": servings["metric_serving_unit"][i],
            }

            food_servings_in_cache = cache[food_id]["servings"]["serving"]
            if isinstance(food_servings_in_cache, dict):
                food_servings_in_cache = [food_servings_in_cache]

            for serving in food_servings_in_cache:
                if serving["serving_id"] == new_serving["serving_id"]:
                    serving.update(new_serving)
                    break

        with open(self.servings, "wb") as f:
            pickle.dump(cache, f)

    def get_daily_total(
        self, user_id, entry_date: datetime
    ) -> Union[dict, None]:
        """добыча из кеша суммарного количества и калорий съеденной еды
        по названиям за один день в виде словаря:
        {'food_name': {'total_calories': ..., 'total_amount': ... , 'metric': ...}}
        """

        entry_date = entry_date.date()

        with open(self.daily_total_cache, "rb") as file:
            cache = pickle.load(file)

        if cache.get(user_id):
            if cache[user_id].get(entry_date):
                daily_total = cache[user_id][entry_date]
                return daily_total

        return {}

    def save_daily_total(
        self, user_id: int, entry_date: datetime, daily_total: dict
    ) -> None:
        """сохранение в кеше суммарного количества и калорий
        съеденной еды по названиям за один день для ускорения создания топов
        записываются даты старше 2 дней и единожды
        """

        # если есть no_metric, не сохраняем
        if daily_total.get("no_metric"):
            return

        # если прошло меньше 3 дней, не сохраняем
        entry_date = entry_date.date()
        if (date.today() - entry_date).days < 3:
            return

        with open(self.daily_total_cache, "rb") as file:
            cache = pickle.load(file)

        if cache.get(user_id):
            if cache[user_id].get(entry_date):
                return
            else:
                cache[user_id].update({entry_date: daily_total})
        else:
            cache.update({user_id: {entry_date: daily_total}})

        with open(self.daily_total_cache, "wb") as file:
            pickle.dump(cache, file)

    def get_monthly_total(
        self, user_id, entry_month: datetime
    ) -> Union[dict, None]:
        """добыча из кеша суммарного количества и калорий съеденной еды
        по названиям за один месяц в виде словаря:
        {'food_name': {'total_calories': ..., 'total_amount': ... , 'metric': ...}}
        """

        entry_month = entry_month.strftime("%Y-%m")

        with open(self.monthly_total_cache, "rb") as file:
            cache = pickle.load(file)

        if cache.get(user_id):
            if cache[user_id].get(entry_month):
                monthly_total = cache[user_id][entry_month]
                return monthly_total

        return {}

    def save_monthly_total(
        self, user_id, entry_month: datetime, monthly_total: dict
    ) -> None:
        """сохранение в кеше суммарного количества и калорий
        съеденной еды по названиям за один день для ускорения создания топов
        записываются даты старше 2 дней и единожды
        """

        # если есть no_metric, не сохраняем
        if monthly_total.get("no_metric"):
            return

        # если прошло меньше 3 дней, не сохраняем
        if (date.today() - entry_month.date()).days < 3:
            return

        entry_month = entry_month.strftime("%Y-%m")
        current_month = date.today().strftime("%Y-%m")

        # если месяц - текущий, не сохраняем
        if entry_month == current_month:
            return

        with open(self.monthly_total_cache, "rb") as file:
            cache = pickle.load(file)

        # если такого юзера еще не записано - сохраняем
        if cache.get(user_id) is None:
            cache.update({user_id: {entry_month: monthly_total}})

            with open(self.monthly_total_cache, "wb") as file:
                pickle.dump(cache, file)

        # если такой юзер записан, но нет такого месяца - сохраняем
        if cache[user_id].get(entry_month) is None:
            cache[user_id].update({entry_month: monthly_total})

            with open(self.monthly_total_cache, "wb") as file:
                pickle.dump(cache, file)


# fs = FatsecretCacheManager()
# fs._remove_prods_no_metric()
# fs._create_caches()
