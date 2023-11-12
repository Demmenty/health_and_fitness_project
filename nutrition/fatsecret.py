from datetime import date, datetime
from home.cache import weak_lru
from typing import Union
from collections import defaultdict
from fatsecret import Fatsecret

from config.settings import FS_CONSUMER_KEY, FS_CONSUMER_SECRET
from home.utils import convert_epoch_to_date, convert_to_datetime
from nutrition.cache import FatsecretCacheManager
from nutrition.models import FatSecretEntry
from users.models import User

fs_cache = FatsecretCacheManager()

NUTRITION_PARAMS = ("calories", "protein", "fat", "carbohydrate")


class FSManager:
    """Functions for working with FatSecret API."""

    session: Fatsecret = Fatsecret(FS_CONSUMER_KEY, FS_CONSUMER_SECRET)
    clients_sessions: dict = {}
    client_id: int | None = None

    def __init__(self, entry_data: FatSecretEntry):
        """
        Initializes an instance and session specific to a client.

        Args:
            entry_data (FatSecretEntry): An instance of the FatSecretEntry class.
        """
        client_token = (entry_data.oauth_token, entry_data.oauth_token_secret)
        self.session = Fatsecret(
            FS_CONSUMER_KEY, FS_CONSUMER_SECRET, client_token
        )
        self.client_id = entry_data.client.id

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

    def save_session(self) -> None:
        """Saves the session for a specific client."""

        self.clients_sessions[self.client_id] = self.session

    def load_session(self, client_id: int) -> None:
        """
        Loads the session for a specific client.

        Args:
            client_id (int): The ID of the client.
        """
        self.session = self.clients_sessions[client_id]
        self.client_id = client_id

    def get_daily_food(
        self, day: Union[datetime, date, str] = datetime.now()
    ) -> dict:
        """
        Retrieves the daily food information for a given day from FatSecret.

        Args:
            day (Union[datetime, date, str], optional): The day for which to retrieve the food information. 
                Defaults to the current date.

        Returns:
            dict: A dictionary containing the daily food information.
                "categories" (dict): Food items grouped by meal category.
                "no_metric" (dict): Food items without serving metrics.
        """

        day_datetime = convert_to_datetime(day)

        # try to get from cache first
        # cache if not today or yesterday

        entries = self.session.food_entries_get(date=day_datetime)

        daily_food = {
            "meal": {},
            "no_metric": {},
        }

        for entry in entries:
            all_servings = self._get_servings_by_food_id(entry["food_id"])
            serving = self._get_serving_by_id(entry["serving_id"], all_servings)

            food_item = self._generate_food_item(entry, all_servings, serving)

            category = entry["meal"].lower()
            daily_food["meal"].setdefault(category, []).append(food_item)

            if not food_item.get("amount"):
                additional_info = self._get_info_for_no_metric_item(entry, serving)
                food_item.update(additional_info)
                daily_food["no_metric"][entry["food_id"]] = food_item

        return daily_food

    def get_monthly_food(self, month: Union[datetime, date, str] = datetime.now()) -> dict:
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

        monthly_nutrition = self.get_monthly_nutrition_dict(month)

        if not monthly_nutrition:
            return {}
        
        monthly_food = {
            "days": {},
            "no_metric": {},
        }
        
        for day in monthly_nutrition.keys():
            daily_food = self.get_daily_food(day)
            monthly_food["days"][day] = daily_food
            monthly_food["no_metric"].update(daily_food["no_metric"])
        
        return monthly_food

    def get_monthly_nutrition_dict(self, month: Union[datetime, date, str] = datetime.now()) -> dict:
        """
        Retrieves the nutrition info from client account in Fatsecret for a given month.

        Args:
            month (Union[datetime,date,str], optional): The month for the nutrition.
                Defaults to the current month. Strings in the format "%Y-%m-%d".

        Returns:
            dict[dict]: A dictionary containing the nutrition information for each day of the specified month.
                The keys are the dates and the values are dictionaries containing the following information:
                "calories" (float): The number of calories consumed on that day.
                "protein" (float): The amount of protein consumed on that day.
                "fat" (float): The amount of fat consumed on that day.
                "carbohydrate" (float): The amount of carbohydrates consumed on that day.
                If no nutrition information is available for the specified month, an empty dictionary is returned.
        """
        
        month_datetime = convert_to_datetime(month)

        try:
            entries = self.session.food_entries_get_month(date=month_datetime)
        except KeyError:
            return {}

        if not entries:
            return {}

        if isinstance(entries, dict):
            entries = [entries]

        monthly_nutrition = {
            convert_epoch_to_date(int(entry["date_int"])): {
                param: float(entry.get(param, 0))
                for param in NUTRITION_PARAMS
            }
            for entry in entries
        }

        return monthly_nutrition

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
        month_datetime = convert_to_datetime(month)

        try:
            entries = self.session.food_entries_get_month(date=month_datetime)
        except KeyError:
            return []

        if not entries:
            return []

        if isinstance(entries, dict):
            entries = [entries]

        monthly_nutrition = []

        for entry in entries:
            day_nutrition = {
                "date": convert_epoch_to_date(int(entry["date_int"])),
                **{param: float(entry.get(param, 0)) for param in NUTRITION_PARAMS}
            }
            monthly_nutrition.append(day_nutrition)

        return monthly_nutrition

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

        total_amount = sum(
            food["amount"] for food in all_food
            if food.get("amount")
        )
        return total_amount

    def calc_monthly_avg_nutrition(
        self, monthly_nutrition: list[dict]|dict[dict], count_today: bool = True) -> dict:
        """
        Calculates the average nutrition for a given month based on the provided monthly nutrition data.

        Args:
            monthly_nutrition (list[dict]|dict[dict]): The monthly nutrition data. 
                It can be either a list of dictionaries or a dictionary of dictionaries.
            count_today (bool, optional): Determines whether to include today's data in the calculation. Defaults to True.

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
                day_nutr for day_nutr in monthly_nutrition
                if day_nutr["date"] != date.today()
            ]

        days = len(monthly_nutrition)

        avg_nutrition = {
            param: round(sum(float(day.get(param, 0)) for day in monthly_nutrition)/ days, 2)
            for param in NUTRITION_PARAMS
        }

        return avg_nutrition

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

        sort_key = lambda item: item[1][parameter] if item[1][parameter] is not None else 0
        sorted_food = sorted(totals.items(), key=sort_key, reverse=True)
        top_food = sorted_food[:limit]

        numerated_top = {
            i+1: {
                "name": name, 
                "calories": data["calories"], 
                "amount": data["amount"], 
                "serving_unit": data["serving_unit"],
            } 
            for i, (name, data) in enumerate(top_food)
        }
        return numerated_top

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

        totals = defaultdict(lambda: {
            "serving_unit": None,
            "amount": None,
            "calories": None,
            "protein": None,
            "fat": None,
            "carbohydrate": None,
        })

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

    def _generate_food_item(
        self, entry: dict, all_servings: dict, serving: dict
    ) -> dict:
        """
        Generates a food item dictionary based on the given food entry, 
        all servings, and serving related to the food.

        Args:
            entry (dict): A dictionary containing information about the food.
            all_servings (dict): A dictionary containing information about all servings.
            serving (dict): A dictionary containing information about the serving.

        Returns:
            dict: The generated food item dictionary.
                "name" (str): The name of the particular food.
                "common_name" (str): A more common name of the food.
                "amount" (int): The amount of food consumed.
                "serving_unit" (str): The unit of measurement for the serving.
                "calories" (float): The number of calories in the food.
                "protein" (float): The amount of protein in the food.
                "fat" (float): The amount of fat in the food.
                "carbohydrate" (float): The amount of carbohydrates in the food.
        """
        food_item = {
            "name": entry["food_entry_name"],
            "common_name": all_servings.get("food_name"),
            "amount": self._get_food_amount(entry, serving),
            "serving_unit": serving.get("metric_serving_unit"),
            "calories": entry["calories"],
            "protein": entry["protein"],
            "fat": entry["fat"],
            "carbohydrate": entry["carbohydrate"],
        }
        return food_item

    def _get_info_for_no_metric_item(self, entry: dict, serving: dict) -> dict:
        """
        Generate additional information for a food item without serving metrics.

        Args:
            entry (dict): The food entry from FS containing the food information.
            serving (dict): The serving information of this food item.

        Returns:
            dict: The generated information for the non-metric item.
                "serving_description" (str): The description of the serving.
                "serving_id" (str): The ID of the serving.
                "calories_per_serving" (float): The number of calories per serving.
        """
        info = {
            "serving_description": serving.get(
                "serving_description", "порция"
            ),
            "serving_id": serving["serving_id"],
            "calories_per_serving": int(entry["calories"])
            / float(entry["number_of_units"]),
        }
        return info

    def _get_servings_by_food_id(self, food_id: str) -> dict:
        """
        Retrieves all servings of a specific food item by its ID.

        Args:
            food_id (str): The unique identifier of the food item in FatSecret.

        Returns:
            dict: A dictionary with the keys 'food_name' and 'servings'.
            If the food information cannot be retrieved, an empty dictionary is returned.
        """
        servings = fs_cache.get_servings(food_id)

        if not servings:
            try:
                servings = self.session.food_get(food_id)
                fs_cache.save_servings(servings)
            except Exception:
                servings = {}

        return servings
    
    def _get_serving_by_id(self, serving_id: str, servings: dict) -> dict | None:
        """
        Get the food entry serving information based on the serving ID.
        
        Parameters:
            serving_id (int): The ID of the serving.
            servings (dict): The dictionary containing all servings information related to the food.
        
        Returns:
            dict: The serving information for the specified serving ID.
        """
        servings = servings["servings"]["serving"]

        if isinstance(servings, dict):
            return servings

        if isinstance(servings, list):
            for serving in servings:
                if serving["serving_id"] == serving_id:
                    return serving

    def _get_food_amount(self, entry:dict, serving:dict) -> int | None:
        """
        Calculates the amount of food in grams or milliliters based on 
        the food entry from FS and information of its serving.

        Parameters:
            entry (dict): A dictionary containing information about the food entry.
            serving (dict): A dictionary containing information about the serving.

        Returns:
            int | None: The amount of food in grams or milliliters, or None.
        """
        measurement = serving.get("measurement_description")
        if measurement in ["g", "ml"]:
            return int(float(entry["number_of_units"]))
        
        serving_amount = serving.get("metric_serving_amount")
        if serving_amount:
            food_units = float(entry["number_of_units"])
            serving_units = float(serving["number_of_units"])
            return int(food_units * float(serving_amount) * serving_units)
