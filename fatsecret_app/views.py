from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from fatsecret import GeneralError

from common.cache_manager import cache
from common.services import services

from .services import *


def fatsecretauth(request):
    """Привязка пользователя к его аккаунту FatSecret"""

    callback_url = settings.CURRENT_DOMAIN + "/fatsecret_app/auth/"

    # 1) получаем адрес подключения и направляем по нему
    if request.GET.get("oauth_verifier") is None:
        auth_url = services.fs.session.get_authorize_url(
            callback_url=callback_url
        )

        return redirect(auth_url)

    # 2) получаем ключи от FatSecret
    if request.GET.get("oauth_verifier"):
        verifier_pin = request.GET.get("oauth_verifier")

        try:
            # тут иногда возникает ошибка - не смогла понять причину
            session_token = services.fs.session.authenticate(verifier_pin)
            services.fs.save_token(session_token, request.user)
            return redirect("mealjournal_page")

        except KeyError as error:
            print("загадочная ошибка, пробуем снова", error)
            auth_url = services.fs.session.get_authorize_url(
                callback_url=callback_url
            )
            return redirect(auth_url)


@login_required
@require_http_methods(["POST"])
def foodmetricsave(request):
    """Сохранение введенной метрики еды через ajax"""

    prods_without_metric = dict(request.POST)
    del prods_without_metric["csrfmiddlewaretoken"]

    cache.fs.save_foodmetric(prods_without_metric)

    return HttpResponse("метрика сохранена. круто!")


@login_required
@require_http_methods(["GET"])
def get_monthly_top(request):
    """выдает топ-10 продуктов месяца через ajax"""

    month = request.GET.get("month")
    if not month:
        return HttpResponseBadRequest("Необходимо передать month")

    try:
        month = datetime.strptime(month, "%Y-%m-%d")
    except ValueError as error:
        return HttpResponseBadRequest(error)

    if request.user.is_expert:
        client_id = request.GET.get("client_id")
        if not client_id:
            return HttpResponseBadRequest("Необходимо передать client_id")
    else:
        client_id = request.user.id

    try:
        monthly_top = services.fs.monthly_top(client_id, month)
    except GeneralError as error:
        return HttpResponseServerError(error)

    data = {
        "monthly_top": monthly_top,
    }
    return JsonResponse(data, status=200)
