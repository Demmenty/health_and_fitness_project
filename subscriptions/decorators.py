from functools import wraps

from django.http import HttpResponseForbidden

from subscriptions.models import Subscription


def require_access(access_levels):
    """
    A decorator to make a view available only for certain subscription access levels.

    Args:
        access_levels: list of access levels that are allowed for the view.
            Options: ["NUTRITION", "TRAINING", "FULL"]
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_expert:
                return func(request, *args, **kwargs)

            subscription: Subscription = getattr(request.user, "subscription", None)
            if not subscription or subscription.plan.access not in access_levels:
                return HttpResponseForbidden("Нет доступа к данному разделу")

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
