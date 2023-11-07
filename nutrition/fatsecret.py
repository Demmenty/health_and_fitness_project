from datetime import date, datetime
from home.cache import weak_lru
from typing import Union

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

    def get_daily_total_nutrition(
        self, day: Union[datetime, date, str] = datetime.now()
    ) -> dict:
        """
        Retrieves the nutrition info from client account in Fatsecret for a given day.

        Args:
            day (datetime|date|str, optional): The date for the nutrition.
                Defaults to the current datetime. Strings in the format "%Y-%m-%d".

        Returns:
            dict: A dictionary containing the following nutrition information:
                "calories" (float): The total of calories consumed.
                "protein" (float): The total of protein consumed.
                "fat" (float): The total of fat consumed.
                "carbohydrate" (float): The total of carbohydrates consumed.
        """

        day_datetime = convert_to_datetime(day)
        entries = self.session.food_entries_get(date=day_datetime)

        if not entries:
            return {}

        return self._calc_daily_total_nutrition(entries)

    def get_monthly_nutrition(
        self, month: Union[datetime, date, str] = datetime.now()
    ) -> dict[dict]:
        """
        Retrieves the nutrition info from client account in Fatsecret for a given month.

        Args:
            month (Union[datetime,date,str], optional): The month for the nutrition.
                Defaults to the current month. Strings in the format "%Y-%m".

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

        return self._calc_monthly_nutrition(entries)

    def get_daily_food(
        self, day: Union[datetime, date, str] = datetime.now()
    ) -> dict:
        """
        Retrieves the daily food information for a given day from FatSecret.

        Args:
            day (Union[datetime, date, str], optional): The day for which to retrieve the food information. 
                Defaults to the current date and time.

        Returns:
            dict: A dictionary containing the daily food information.
                "meal" (dict): A dictionary of food items grouped by meal category.
                "no_metric" (dict): A dictionary of food items without metric information.
                "total_nutrition" (dict): A dictionary containing the total nutrition information.
                "total_amount" (float): The total amount of food consumed (grams or milliliters).
        """
        day_datetime = convert_to_datetime(day)
        entries = self.session.food_entries_get(date=day_datetime)

        if not entries:
            return {}

        daily_food = self._generate_daily_food_dict(entries)
        daily_food["total_nutrition"] = self._calc_daily_total_nutrition(entries)
        daily_food["total_amount"] = self._calc_total_amount(daily_food)

        return daily_food

    def _generate_daily_food_dict(self, entries: list) -> dict:
        """
        Generates a daily food dictionary based on a list of food entries.

        Args:
            entries (list): The list of food entries from FatSecret.

        Returns:
            dict: The daily food dictionary.
                "meal" (dict): A dictionary of food items grouped by meal category.
                "no_metric" (dict): A dictionary of food items without metric information.
        """
        daily_food = {
            "meal": {},
            "no_metric": {},
        }

        for entry in entries:
            all_servings = self._get_servings_by_food_id(entry["food_id"])
            serving = self._get_serving_by_id(entry["serving_id"], all_servings)

            food_item = self._generate_food_item(entry, all_servings, serving)

            meal_category = entry["meal"].lower()
            daily_food["meal"].setdefault(meal_category, []).append(food_item)

            if not food_item.get("amount"):
                additional_info = self._get_info_for_no_metric_item(entry, serving)
                food_item.update(additional_info)
                daily_food["no_metric"][entry["food_id"]] = food_item

        return daily_food

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

    def _calc_total_amount(self, daily_food: dict) -> int:
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
        total_amount = sum(
            food_item["amount"]
            for food_items in daily_food["meal"].values()
            for food_item in food_items
            if food_item.get("amount")
        )
        return total_amount

    def _calc_daily_total_nutrition(self, entries: list[dict]) -> dict:
        """
        Calculate the total nutrition of a list of daily food entries.
        Values are rounded to two decimal places.

        Args:
            entries (list): A list of dictionaries containing the following keys:
                calories (float): The number of calories in the food entry.
                protein (float): The amount of protein in the food entry.
                fat (float): The amount of fat in the food entry.
                carbohydrate (float): The amount of carbohydrates in the food entry.

        Returns:
            dict: A dictionary containing the following keys:
                calories (float): The total number of calories from all the food entries.
                protein (float): The total amount of protein from all the food entries.
                fat (float): The total amount of fat from all the food entries.
                carbohydrate (float): The total amount of carbohydrates from all the food entries.
        """
        total_nutrition = {
            key: round(
                sum(float(entry.get(key, 0)) for entry in entries), 2
            )
            for key in NUTRITION_PARAMS
        }
        return total_nutrition

    def _calc_monthly_nutrition(self, entries: list[dict]) -> dict:
        """
        Calculate the monthly nutrition based on a list of entries for a month.
`
        Args:
            entries (list[dict]): A list of dictionaries representing nutrition daily entries.
                Each dictionary should have the following keys:
                "date_int" (int): The number of days since 1970.
                "calories" (float): The number of calories consumed on that day.
                "protein" (float): The amount of protein consumed on that day.
                "fat" (float): The amount of fat consumed on that day.
                "carbohydrate" (float): The amount of carbohydrates consumed on that day.

        Returns:
            dict: A dictionary containing the calculated nutrition for each day of the entries.
                The keys are the dates and the values are dictionaries containing the following keys:
                "calories" (float): The number of calories consumed on that day.
                "protein" (float): The amount of protein consumed on that day.
                "fat" (float): The amount of fat consumed on that day.
                "carbohydrate" (float): The amount of carbohydrates consumed on that day.
        """
        monthly_nutrition = {}

        for entry in entries:
            date = convert_epoch_to_date(int(entry["date_int"]))
            nutrition = {
                param: float(entry.get(param, 0))
                for param in NUTRITION_PARAMS
            }
            monthly_nutrition[date] = nutrition

        return monthly_nutrition
