from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseBadRequest, HttpResponseForbidden


class ClientOrExpertRequiredMixin(AccessMixin):
    """Запрос разрешен от лица самого клиента либо эксперта"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Необходима авторизация")

        if request.method == "GET":
            client_id = request.GET.get("client")
        elif request.method == "POST":
            client_id = request.POST.get("client")

        if not client_id:
            return HttpResponseBadRequest("Необходим client_id")

        if not request.user.is_expert:
            if request.user.id != int(client_id):
                return HttpResponseForbidden("У вас нет прав на это действие")

        return super().dispatch(request, *args, **kwargs)
