from datetime import date, timedelta


def create_list_of_dates(days: int) -> list:
    """"""

    list_of_dates = []

    for i in range(days):
        selected_date = date.today() - timedelta(days=(6-i))
        list_of_dates.append(selected_date)

    return list_of_dates
