from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

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

    prods_without_metric= dict(request.POST)
    del prods_without_metric["csrfmiddlewaretoken"]

    cache.fs.save_foodmetric(prods_without_metric)

    return HttpResponse("метрика сохранена. круто!")


def get_monthly_top(request):
    """выдает топ-10 продуктов месяца через ajax"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    if request.GET.get("client_id"):
        # если запрос от эксперта о клиенте
        client_id = request.GET.get("client_id")
        client = User.objects.get(id=client_id)
    else:
        # если запрос от самого клиента
        client = request.user

    month_str = request.GET.get("month")
    month_datetime = datetime.strptime(month_str, "%Y-%m")

    monthly_top = services.fs.monthly_top(client, month_datetime)

    return JsonResponse(monthly_top, status=200)
