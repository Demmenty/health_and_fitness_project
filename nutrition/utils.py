from nutrition.dataclasses import FoodDetails, Serving


def parse_food_details(fs_food_details: dict) -> FoodDetails:
    """
    Parse the food details from a dictionary of food info provided by FatSecret API.

    Args:
        fs_food_details (dict): A dictionary containing the food details.
            It should have the following keys: "food_name", "servings".

    Returns:
        FoodDetails: A dataclass object representing the parsed food details.
    """

    common_name = fs_food_details.get("food_name")
    servings = fs_food_details["servings"]["serving"]

    if isinstance(servings, dict):
        servings = [servings]

    food_details = FoodDetails(
        common_name=common_name,
        servings={
            serving["serving_id"]: Serving(
                serving_description=serving.get("serving_description"),
                metric_serving_amount=serving.get("metric_serving_amount"),
                metric_serving_unit=serving.get("metric_serving_unit"),
                measurement_description=serving.get("measurement_description"),
                number_of_units=serving.get("number_of_units"),
            )
            for serving in servings
        },
    )
    return food_details
