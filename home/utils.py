from datetime import date, datetime, time, timedelta
from typing import Union

from django.http import HttpRequest

from users.models import User


def get_client(request: HttpRequest) -> User | None:
    """
    Returns the client from the given HttpRequest based on the user type.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Optional[User]: The client information if found, None otherwise.
    """

    if request.user.is_expert:
        return request.GET.get("client")
    return request.user


def is_ajax(request: HttpRequest) -> bool:
    """
    Check if a request is an AJAX request.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        bool: True if the request is an AJAX request, False otherwise.
    """

    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def get_noun_ending(number: int, one: str, two: str, five: str) -> str:
    """
    Given a number, returns a variant of a word with the correct ending for russian language.
    You need to pass corresponding options.
    Example: get_noun_ending(4, 'слон', 'слона', 'слонов'))

    Args:
    - `number` : int - The number for which the noun ending needs to be determined.
    - `one` : str - The noun ending for numbers ending in 1.
    - `two` : str - The noun ending for numbers ending in 2, 3, or 4.
    - `five` : str - The noun ending for numbers ending in 0 or 5-9.
    Returns:
        - str - The appropriate noun ending based on the input number.
    """

    n = abs(number) % 100

    if 20 >= n >= 5:
        return five

    n %= 10
    if n == 1:
        return one

    if 4 >= n >= 2:
        return two

    return five


def convert_date_to_epoch(request_date: date) -> int:
    """Converts date into number of days since 1970"""

    return str((request_date - date(1970, 1, 1)).days)


def convert_epoch_to_date(date_epoch: int) -> date:
    """Converts number of days since 1970 into date"""

    return date(1970, 1, 1) + timedelta(days=date_epoch)


def convert_to_datetime(input_date: Union[datetime, date, str]) -> datetime:
    """
    Convert the input date type to a datetime type.

    Args:
        input_date (datetime|date|str): The date to be converted.
        It can be a `datetime`, `date`, or a string in the format "%Y-%m-%d".
    Returns:
        datetime: The datetime object.
    """

    if isinstance(input_date, str):
        return datetime.strptime(input_date, "%Y-%m-%d")
    elif isinstance(input_date, date):
        return datetime.combine(input_date, time())
    return input_date
