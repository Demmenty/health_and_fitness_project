from datetime import date, datetime, time, timedelta


def get_noun_ending(number, one, two, five) -> str:
    """возвращает вариант слова с правильным окончанием в зависимости от числа
    Нужно передать число и соответствующие варианты
    например: get_noun_ending(4, 'слон', 'слона', 'слонов'))
    """
    n = abs(number)
    n %= 100
    if 20 >= n >= 5:
        return five
    n %= 10
    if n == 1:
        return one
    if 4 >= n >= 2:
        return two
    return five


# date_manipulations (найти, мб уже есть такое в datetime)
def date_into_epoch(request_date: date) -> int:
    """превращает datetime в число дней с 1970"""

    date_int = str((request_date - date(1970, 1, 1)).days)

    return date_int


def epoch_into_datetime(date_epoch: int) -> datetime:
    """конвертирует число дней с 1970 в datetime"""

    date_date = date(1970, 1, 1) + timedelta(days=date_epoch)
    date_datetime = datetime.combine(date_date, time())

    return date_datetime


def datetime_into_epoch(request_date: datetime) -> int:
    """превращает datetime в число дней с 1970"""

    date_int = str((request_date.date() - date(1970, 1, 1)).days)

    return date_int
