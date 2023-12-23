from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from main.utils import is_ajax


def client_required(view_func):
    """
    Decorator that checks if the user is authenticated and not an expert.
    If not, redirects to the home page or returns a return forbidden response for AJAX requests.

    Args:
        view_func (function): The view function to be decorated.
    Returns:
        function: The decorated view function.
    """

    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_expert:
            if is_ajax(request):
                return HttpResponseForbidden("Недостаточно прав!")
            return redirect("main:home")

        return view_func(request, *args, **kwargs)

    return wrapper_func
