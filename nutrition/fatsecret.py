from collections import defaultdict
from datetime import date, datetime
from typing import Union

from fatsecret import Fatsecret

from config.settings import FS_CONSUMER_KEY, FS_CONSUMER_SECRET
from main.utils import convert_epoch_to_date, convert_to_datetime
from nutrition.cache import FSCacheManager
from nutrition.dataclasses import FoodDetails, Serving
from nutrition.models import FatSecretEntry
from nutrition.utils import parse_food_details
from users.models import User

fs_cache = FSCacheManager()

NUTRITION_PARAMS = ("calories", "protein", "fat", "carbohydrate")


class FSManager:
    """Functions for working with FatSecret API"""

    session: Fatsecret
    clients_sessions: dict = {}
    client_id: int | None

    def __init__(self, client_entry: FatSecretEntry = None):
        """
        Initializes an instance and session for work with FatSecret API.
        If client_entry is provided, it loads the session specific to a client.
        (And allows to interact with client's FS account and methods).

        Args:
            client_entry (FatSecretEntry): An instance of the FatSecretEntry class
                with client's credentials. Defaults to None.
        """

        if client_entry:
            client_token = (client_entry.oauth_token, client_entry.oauth_token_secret)
            self.session = Fatsecret(FS_CONSUMER_KEY, FS_CONSUMER_SECRET, client_token)
            self.client_id = client_entry.client.id
        else:
            self.session = Fatsecret(FS_CONSUMER_KEY, FS_CONSUMER_SECRET)
            self.client_id = None

    def save_tokens(self, client_tokens: tuple, client: User) -> None:
        """Save tokens for interacting with client's FS account in the database."""

        oauth_token, oauth_token_secret = client_tokens

        FatSecretEntry.objects.update_or_create(
            client=client,
            defaults={
                "oauth_token": oauth_token,
                "oauth_token_secret": oauth_token_secret,
            },
        )

    def save_session(self, client_id: int) -> None:
        """
        Saves the session for a specific client.

        Args:
            client_id (int): The ID of the client.
        """

        self.clients_sessions[client_id] = self.session

    def load_session(self, client_id: int) -> None:
        """
        Loads the session for a specific client.

        Args:
            client_id (int): The ID of the client.
        """

        self.session = self.clients_sessions[client_id]
        self.client_id = client_id

    def get_daily_food(self, day: Union[datetime, date, str] = datetime.now()) -> dict:
        """
        Retrieves the daily food information for a given day.

        Args:
            day (Union[datetime, date, str], optional): The day for which to retrieve the food information.
                Defaults to the current date.

        Returns:
            dict: A dictionary containing the daily food information.
                "categories" (dict): Food items grouped by meal category.
                "no_metric" (dict): Food items without serving metrics.
        """

        day = convert_to_datetime(day)
        if day > datetime.now():
            return {}

        daily_food = fs_cache.get_daily_food(self.client_id, day)
        if not daily_food is None:
            return daily_food

        entries: list[dict] = self.session.food_entries_get(date=day)

        daily_food = {"meal": {}, "no_metric": {}}

        for entry in entries:
            food_id = entry["food_id"]
            food_details: FoodDetails = self.get_food_details(food_id)

            serving_id = entry["serving_id"]
            serving: Serving = food_details.servings.get(serving_id)

            number_of_units = float(entry["number_of_units"])
            food_amount = self.calc_food_amount(number_of_units, serving)

            food_item = {
                "name": entry.get("food_entry_name"),
                "common_name": food_details.common_name,
                "amount": food_amount,
                "serving_unit": serving.metric_serving_unit,
                "calories": entry.get("calories"),
                "protein": entry.get("protein"),
                "fat": entry.get("fat"),
                "carbohydrate": entry.get("carbohydrate"),
            }

            if not food_amount:
                serving_description = serving.serving_description or "порция"
                calories_per_serving = int(entry["calories"]) / number_of_units
                food_item.update(
                    {
                        "serving_description": serving_description,
                        "serving_id": serving_id,
                        "calories_per_serving": calories_per_serving,
                    }
                )
                daily_food["no_metric"][food_id] = food_item

            meal_category = entry.get("meal").lower()
            daily_food["meal"].setdefault(meal_category, []).append(food_item)

        if not daily_food.get("no_metric"):
            if fs_cache.is_day_saveable(day):
                fs_cache.save_daily_food(self.client_id, day, daily_food)

        return daily_food

    def get_monthly_food(
        self, month: Union[datetime, date, str] = datetime.now()
    ) -> dict:
        """
        Retrieves the monthly food information for a given month.

        Args:
            month (Union[datetime, date, str], optional): The month for which to retrieve the food information.
                Defaults to the current month.

        Returns:
            dict: A dictionary containing the monthly food information.
                "days" (dict): Food information for each day of the month.
                "no_metric" (dict): Food items without serving metrics.
        """

        month = convert_to_datetime(month)
        if month > datetime.now():
            return {}

        monthly_food = fs_cache.get_monthly_food(self.client_id, month)
        if not monthly_food is None:
            return monthly_food

        monthly_nutrition: dict = self.get_monthly_nutrition_dict(month)

        monthly_food = {"days": {}, "no_metric": {}}

        for day in monthly_nutrition.keys():
            daily_food = self.get_daily_food(day)
            monthly_food["days"][day] = daily_food
            monthly_food["no_metric"].update(daily_food["no_metric"])

        if not monthly_food.get("no_metric"):
            if fs_cache.is_month_saveable(month):
                fs_cache.save_monthly_food(self.client_id, month, monthly_food)

        return monthly_food

    def get_monthly_entries(self, month: datetime) -> list:
        """
        Retrieves the monthly entries of client's nutrition for a given month.

        Args:
            month (datetime): The date of the month for which to retrieve the entries.

        Returns:
            list: A list of monthly entries (dictionaries) for the given month.
        """

        if month > datetime.now():
            return []

        monthly_entries = fs_cache.get_monthly_entries(self.client_id, month)

        if monthly_entries is None:
            try:
                monthly_entries = self.session.food_entries_get_month(date=month)
                if isinstance(monthly_entries, dict):
                    monthly_entries = [monthly_entries]
            except KeyError:
                monthly_entries = []

            if fs_cache.is_month_saveable(month):
                fs_cache.save_monthly_entries(self.client_id, month, monthly_entries)

        return monthly_entries

    def get_monthly_nutrition_dict(
        self, month: Union[datetime, date, str] = datetime.now()
    ) -> dict:
        """
        Retrieves the nutrition info from client account in Fatsecret for a given month.

        Args:
            month (datetime, optional): The month for the nutrition.
                Defaults to the current month.

        Returns:
            dict[dict]: A dictionary containing the nutrition information for each day of the specified month.
                The keys are the dates and the values are dictionaries containing the following information:
                "calories" (float): The number of calories consumed on that day.
                "protein" (float): The amount of protein consumed on that day.
                "fat" (float): The amount of fat consumed on that day.
                "carbohydrate" (float): The amount of carbohydrates consumed on that day.
                If no nutrition information is available for the specified month, an empty dictionary is returned.
        """

        month = convert_to_datetime(month)
        monthly_entries = self.get_monthly_entries(month)

        return {
            convert_epoch_to_date(int(entry["date_int"])): {
                param: float(entry.get(param, 0)) for param in NUTRITION_PARAMS
            }
            for entry in monthly_entries
            if entry.get("calories") != "0"
        }

    def get_monthly_nutrition_list(
        self, month: Union[datetime, date, str] = datetime.now()
    ) -> list[dict]:
        """
        Retrieves the nutrition info from client account in Fatsecret for a given month.

        Args:
            month (Union[datetime,date,str], optional): The month for the nutrition.
                Defaults to the current month. Strings in the format "%Y-%m-%d".

        Returns:
            list[dict]: A list containing the nutrition information for each day of the specified month.
                Each dictionary in the list represents a day and contains the following information:
                "day" (datetime.date): The date of the day.
                "calories" (float): The number of calories consumed on that day.
                "protein" (float): The amount of protein consumed on that day.
                "fat" (float): The amount of fat consumed on that day.
                "carbohydrate" (float): The amount of carbohydrates consumed on that day.
        """

        month = convert_to_datetime(month)
        monthly_entries = self.get_monthly_entries(month)

        return [
            {
                "date": convert_epoch_to_date(int(entry["date_int"])),
                **{param: float(entry.get(param, 0)) for param in NUTRITION_PARAMS},
            }
            for entry in monthly_entries
            if entry.get("calories") != "0"
        ]

    def get_food_details(self, food_id: str) -> FoodDetails | None:
        """
        Retrieves the details of a specific food item.
        Such as common name and serving information.

        Parameters:
            food_id (str): The unique identifier of the food item.

        Returns:
            FoodDetails | None: The details of the food item,
                or None if the details are not available.
        """

        food_details = fs_cache.get_food_details(food_id)

        if food_details is None:
            fs_food_details = self.session.food_get(food_id)
            food_details = parse_food_details(fs_food_details)
            fs_cache.save_food_details(food_id, food_details)

        return food_details

    def calc_food_amount(self, number_of_units: float, serving: Serving) -> int | None:
        """
        Calculates the amount of food based on the number of units and serving information.

        Args:
            number_of_units (float): The number of units of the food entry.
            serving (Serving): The serving information of the food.

        Returns:
            int | None: The calculated amount of food in grams or milliliters.
                If the serving measurement is not in grams or milliliters, returns None.
        """

        if serving.measurement_description in ["g", "ml"]:
            return number_of_units

        serving_amount = serving.metric_serving_amount
        if serving_amount:
            serving_units = float(serving.number_of_units)
            return int(number_of_units * float(serving_amount) * serving_units)

    def calc_daily_total_nutrition(self, daily_food: dict) -> dict:
        """
        Calculates the total nutrition of food consumed in a day.

        Args:
            daily_food (dict): A dictionary containing the daily food consumption.
                "meal" (dict): A dictionary of food items grouped by meal category.

        Returns:
            dict: A dictionary containing the following keys:
                calories (float): The total number of calories from all the food entries.
                protein (float): The total amount of protein from all the food entries.
                fat (float): The total amount of fat from all the food entries.
                carbohydrate (float): The total amount of carbohydrates from all the food entries.
        """

        if not daily_food:
            return {}

        all_food = []
        for food_list in daily_food["meal"].values():
            all_food.extend(food_list)

        total_daily_nutrition = {
            param: round(sum(float(food.get(param, 0)) for food in all_food), 2)
            for param in NUTRITION_PARAMS
        }
        return total_daily_nutrition

    def calc_daily_total_amount(self, daily_food: dict) -> int:
        """
        Calculate the total amount of food consumed in a day.

        Args:
            daily_food (dict): A dictionary representing the daily food consumption.
                It should have the following structure:
                {
                    "meal": {
                        "breakfast": [food_item, food_item, ...],
                        "lunch": [food_item, food_item, ...],
                        ...
                    }
                }
                Each food_item should have the "amount" key indicating the amount of food consumed.
                If the food item does not have an "amount" key, it will be ignored.

        Returns:
            int: The total amount of food consumed in a day (grams or milliliters).
        """

        if not daily_food:
            return 0

        all_food = []
        for food_list in daily_food["meal"].values():
            all_food.extend(food_list)

        total_amount = sum(food["amount"] for food in all_food if food.get("amount"))
        return total_amount

    def calc_monthly_avg_nutrition(
        self,
        monthly_nutrition: list[dict] | dict[dict],
        count_today: bool = True,
    ) -> dict:
        """
        Calculates the average nutrition for a given month based on the provided monthly nutrition data.

        Args:
            monthly_nutrition (list[dict]|dict[dict]): The monthly nutrition data.
                It can be either a list of dictionaries or a dictionary of dictionaries.
            count_today (bool, optional): Determines whether to include today's data in the calculation.
                Defaults to True.

        Returns:
            dict: A dictionary containing the average nutrition values for the given month.
            The keys represent the nutrition parameters, and the values are rounded to 2 decimal places.
        """

        if not monthly_nutrition:
            return {}

        if isinstance(monthly_nutrition, dict):
            monthly_nutrition = [
                {"date": day, **nutr} for day, nutr in monthly_nutrition.items()
            ]

        if not count_today:
            monthly_nutrition = [
                day_nutr
                for day_nutr in monthly_nutrition
                if day_nutr["date"] != date.today()
            ]

        days = len(monthly_nutrition)

        if not days:
            return {}

        avg_nutrition = {
            param: round(
                sum(float(day.get(param, 0)) for day in monthly_nutrition) / days,
                2,
            )
            for param in NUTRITION_PARAMS
        }

        return avg_nutrition

    def calc_monthly_food_totals(self, monthly_food: dict) -> dict:
        """
        Calculate the monthly total for each food item in the given monthly food dictionary.
        Totals grouped by food's common name.

        Args:
            monthly_food (dict): A dictionary containing the monthly food data.

        Returns:
            dict: A dictionary containing the monthly totals for each food item.
                The keys are the names of the food items and the values are:
                    "amount": The amount of food consumed in grams or milliliters (if available, else None).
                    "serving_unit": The unit of measure used for the serving.
                    "calories": The total number of calories consumed in kcal.
                    "protein": The total number of protein in grams.
                    "fat": The total number of fat in grams.
                    "carbohydrate": The total number of carbohydrates in grams.
        """

        parameters = NUTRITION_PARAMS + ("amount",)

        totals = defaultdict(
            lambda: {
                "serving_unit": None,
                "amount": None,
                "calories": None,
                "protein": None,
                "fat": None,
                "carbohydrate": None,
            }
        )

        for day in monthly_food["days"].values():
            for meal_category in day["meal"].values():
                for item in meal_category:
                    name = item["common_name"]

                    unit = item.get("serving_unit")
                    if unit is not None:
                        totals[name]["serving_unit"] = unit

                    for param in parameters:
                        value = item.get(param)
                        if value is not None:
                            if totals[name][param] is None:
                                totals[name][param] = float(value)
                            else:
                                totals[name][param] += float(value)

        return totals

    def calc_monthly_top(self, monthly_food: dict, parameter: str, limit: int = 10):
        """
        Calculate the top monthly food items by a given parameter.
        Food items are gruped by common name and sorted based in descending order.

        Args:
            monthly_food (dict): A dictionary representing the food items consumed in a month.
            parameter (str): The parameter to use for determining the top food items.
                Must be one of "amount" or "calories".
            limit (int, optional): The maximum number of top food items to include.
                Defaults to 10.

        Returns:
            numerated_top (dict): A dictionary containing the top food items.
                The keys are rank numbers, and the values are dictionaries with the following keys:
                    "name": The common name of the food item.
                    "calories": The total number of calories consumed in kcal.
                    "amount": The amount of food consumed in grams or milliliters (if available, else None).
                    "serving_unit": The unit of measure used for the serving.
        """

        totals = self.calc_monthly_food_totals(monthly_food)

        sort_key = (
            lambda item: item[1][parameter] if item[1][parameter] is not None else 0
        )
        sorted_food = sorted(totals.items(), key=sort_key, reverse=True)
        top_food = sorted_food[:limit]

        numerated_top = {
            i
            + 1: {
                "name": name,
                "calories": data["calories"],
                "amount": data["amount"],
                "serving_unit": data["serving_unit"],
            }
            for i, (name, data) in enumerate(top_food)
        }
        return numerated_top
