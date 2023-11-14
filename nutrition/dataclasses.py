from collections import defaultdict
from dataclasses import dataclass
from typing import Dict


@dataclass
class Serving:
    serving_description: str = None
    metric_serving_amount: float = None
    metric_serving_unit: str = None
    measurement_description: str = None
    number_of_units: int = None


@dataclass
class FoodDetails:
    common_name: str = None
    servings: Dict[str, Serving] = None

    def __post_init__(self):
        if self.servings is None:
            self.servings = defaultdict(Serving)
