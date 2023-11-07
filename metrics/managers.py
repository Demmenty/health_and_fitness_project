from datetime import date, timedelta

from django.db.models import Manager

from users.models import User


class DailyDataManager(Manager):
    """Manager for handling entries of DailyData model."""

    def get_by_date_range(self, client: User, start: date, end: date) -> tuple:
        """
        Get tuple of daily metrics of client by date range.
        If no metrics for date - returns empty object for this date.

        Args:
            client (User): The client object.
            start (date): The start date of the range.
            end (date): The end date of the range.
        Returns:
            tuple[DailyData]: A tuple of DailyData objects.
        """
        days = (end - start).days + 1
        if days < 1:
            return []

        metrics = self.filter(client=client, date__range=(start, end))
        if len(metrics) == days:
            return tuple(metrics)

        dates = (start + timedelta(days=i) for i in range(days))

        metrics = tuple(
            metrics.filter(date=date).first()
            or self.model(client=client, date=date)
            for date in dates
        )
        return metrics

    def get_by_days(self, client: User, days: int) -> tuple:
        """
        Get tuple of last daily metrics of client for given number of days from today.
        If no metrics for date - returns empty object for this date.

        Args:
            client (User): The client object.
            days (int): The number of days to get.
        Returns:
            tuple[DailyData]: A tuple of DailyData objects.
        """
        dates = [date.today() - timedelta(days=i) for i in range(days)]

        metrics = self.filter(client=client, date__in=dates)
        if len(metrics) == days:
            return tuple(metrics)

        metrics = tuple(
            metrics.filter(date=date).first()
            or self.model(client=client, date=date)
            for date in reversed(dates)
        )
        return metrics
