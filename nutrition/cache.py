import pickle
from datetime import date, datetime, timedelta

from config.settings import BASE_DIR
from nutrition.dataclasses import FoodDetails

CACHE_DIR = BASE_DIR / "nutrition" / "cache"


class FSCacheManager:
    """Functions for working with FatSecret cache."""

    food_details = CACHE_DIR / "food_details.pickle"
    daily_food = CACHE_DIR / "daily_food.pickle"
    monthly_food = CACHE_DIR / "monthly_food.pickle"
    monthly_entries = CACHE_DIR / "monthly_entries.pickle"

    @classmethod
    def initialize_cache_files(cls):
        """
        Checks if the cache files exist.
        Create cache directory and files if they don't.
        """

        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        cache_files = [
            cls.food_details,
            cls.daily_food,
            cls.monthly_food,
            cls.monthly_entries,
        ]

        for cache_file in cache_files:
            if not cache_file.exists():
                with open(cache_file, "wb") as f:
                    pickle.dump({}, f)

    def is_day_saveable(self, day: datetime) -> bool:
        """
        Check if a given day is saveable.
        Day is saveable if it's not today or yesterday.

        Args:
            day (datetime): The day to be checked.

        Returns:
            bool: True if the day is saveable, False otherwise.
        """
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        if day.date() in (today, yesterday):
            return False

        return True

    def is_month_saveable(self, month: datetime) -> bool:
        """
        Determines if a given month is saveable based on the current date.
        Month is saveable if it's not the current month and it's more than 3 days ago.

        Args:
            month (datetime): The month to check for saveability.

        Returns:
            bool: True if the month is saveable, False otherwise.
        """

        given_month = month.strftime("%Y-%m")
        current_month = date.today().strftime("%Y-%m")

        if given_month == current_month:
            return False

        days_difference = (date.today() - month.date()).days

        if days_difference <= 3:
            return False

        return True

    def get_food_details(self, food_id: str) -> FoodDetails | None:
        """
        Get the details of a specific food from cache.

        Args:
            food_id (str): The ID of the food.

        Returns:
            FoodDetails | None: The details of the food if found, None otherwise.
        """

        with open(self.food_details, "rb") as file:
            cache: dict = pickle.load(file)

        food_details = cache.get(food_id)

        return food_details

    def get_daily_food(self, client_id: int, day: datetime) -> dict | None:
        """
        Retrieves the daily food for a specific client on a given day from cache.

        Args:
            client_id (int): The ID of the client.
            day (datetime): The date for which to retrieve the daily food.

        Returns:
            dict | None: A dictionary containing the daily food for the client on the given day,
                or None if daily food for the given day or client is not found.
        """

        with open(self.daily_food, "rb") as file:
            cache: dict = pickle.load(file)

        client_dict: dict = cache.get(client_id)
        if not client_dict:
            return None

        day_str = day.strftime("%Y-%m-%d")
        daily_food = client_dict.get(day_str)

        return daily_food

    def get_monthly_entries(self, client_id: int, month: datetime) -> list | None:
        """
        Retrieve the monthly entries for a specific client and month from cache.

        Args:
            client_id (int): The ID of the client.
            month (datetime): The month for which to retrieve the entries.

        Returns:
            list | None: A list of monthly entries for the specified client and month.
                If no entries are found, returns None.
        """

        with open(self.monthly_entries, "rb") as file:
            cache: dict = pickle.load(file)

        client_dict: dict = cache.get(client_id)
        if not client_dict:
            return None

        month_str = month.strftime("%Y-%m")
        monthly_entries = client_dict.get(month_str)

        return monthly_entries

    def get_monthly_food(self, client_id: int, month: datetime) -> dict | None:
        """
        Retrieves the monthly food data for a specific client and month from cache.

        Args:
            client_id (int): The ID of the client.
            month (datetime): The month for which to retrieve the data.

        Returns:
            dict | None: The monthly food data for the client and month,
                or None if the client or month data is not found.
        """

        with open(self.monthly_food, "rb") as file:
            cache: dict = pickle.load(file)

        client_dict: dict = cache.get(client_id)
        if not client_dict:
            return None

        month_str = month.strftime("%Y-%m")
        monthly_food = client_dict.get(month_str)

        return monthly_food

    def update_food_serving(self, food_id: str, serving_id: str, params: dict) -> None:
        """
        Updates the serving details for a specific food item in the cache.

        Parameters:
            food_id (str): The ID of the food item.
            serving_id (str): The ID of the serving.
            params (dict): A dictionary containing the updated serving details.
        """

        with open(self.food_details, "rb") as file:
            cache: dict = pickle.load(file)

        serving = cache[food_id].servings[serving_id]
        serving.__dict__.update(params)

        with open(self.food_details, "wb") as f:
            pickle.dump(cache, f)

    def save_food_details(self, food_id: str, details: FoodDetails) -> None:
        """
        Save food details to the cache.

        Args:
            food_id (str): The ID of the food.
            details (FoodDetails): The details of the food.
        """

        with open(self.food_details, "rb") as file:
            cache: dict = pickle.load(file)

        cache[food_id] = details

        with open(self.food_details, "wb") as f:
            pickle.dump(cache, f)

    def save_daily_food(self, client_id: int, day: datetime, food: dict) -> None:
        """
        Save daily food for a specific client on a given day to the cache.

        Args:
            client_id (int): The ID of the client.
            day (datetime): The date of the day.
            food (dict): A dictionary containing the food data.
        """

        with open(self.daily_food, "rb") as file:
            cache: dict = pickle.load(file)

        day_str = day.strftime("%Y-%m-%d")

        client_dict = cache.setdefault(client_id, {})
        client_dict[day_str] = food

        with open(self.daily_food, "wb") as file:
            pickle.dump(cache, file)

    def save_monthly_entries(
        self, client_id: int, month: datetime, entries: dict
    ) -> None:
        """
        Save monthly entries for a specific client on a given month to the cache.

        Args:
            client_id (int): The ID of the client.
            month (datetime): The date of the month.
            entries (dict): A dictionary containing the nutrition data with dates.
        """

        with open(self.monthly_entries, "rb") as file:
            cache: dict = pickle.load(file)

        month_str = month.strftime("%Y-%m")

        client_dict = cache.setdefault(client_id, {})
        client_dict[month_str] = entries

        with open(self.monthly_entries, "wb") as file:
            pickle.dump(cache, file)

    def save_monthly_food(self, client_id: int, month: datetime, food: dict) -> None:
        """
        Save monthly food for a specific client on a given month to the cache.

        Args:
            client_id (int): The ID of the client.
            month (datetime): The date of the month.
            food (dict): A dictionary containing the food data.
        """

        with open(self.monthly_food, "rb") as file:
            cache: dict = pickle.load(file)

        month_str = month.strftime("%Y-%m")

        client_dict = cache.setdefault(client_id, {})
        client_dict[month_str] = food

        with open(self.monthly_food, "wb") as file:
            pickle.dump(cache, file)

    @classmethod
    def delete_client_cache(cls, client_id: int) -> None:
        """
        Delete the cache for a specific client.

        Args:
            client_id (int): The ID of the client.
        """

        cache_files = [cls.daily_food, cls.monthly_entries, cls.monthly_food]

        for cache_file in cache_files:
            with open(cache_file, "rb") as file:
                cache: dict = pickle.load(file)

            if client_id in cache:
                del cache[client_id]
                with open(cache_file, "wb") as file:
                    pickle.dump(cache, file)
