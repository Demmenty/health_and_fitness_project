from django.http import HttpRequest
from django.shortcuts import redirect

from config.settings import MAINTENANCE_MODE


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        if MAINTENANCE_MODE:
            if not request.path_info.startswith(("/admin", "/maintenance")):
                return redirect("main:maintenance")

        return self.get_response(request)
