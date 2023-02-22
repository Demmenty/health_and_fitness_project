from django.shortcuts import redirect
from .services import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from common.services import services
from common.cache_manager import cache
from time import sleep


def fatsecretauth(request):
    """Привязка пользователя к его аккаунту FatSecret"""

    callback_url = settings.CURRENT_DOMAIN + "/fatsecret_app/auth/"

    # 1) получаем адрес подключения и направляем по нему
    if request.GET.get('oauth_verifier') is None:

        auth_url = services.fs.session.get_authorize_url(callback_url=callback_url)

        return redirect(auth_url)

    # 2) получаем ключи от FatSecret
    if request.GET.get('oauth_verifier'):

        verifier_pin = request.GET.get('oauth_verifier')

        try:
            # тут иногда возникает ошибка - не смогла понять причину
            session_token = services.fs.session.authenticate(verifier_pin)
            services.fs.save_token(session_token, request.user)
            return redirect('mealjournal')

        except KeyError as error:
            print("загадочная ошибка, пробуем снова", error)
            auth_url = services.fs.session.get_authorize_url(callback_url=callback_url)
            return redirect(auth_url)


def foodmetricsave(request):
    """Сохранение введенной метрики еды через ajax"""

    if request.user.is_anonymous:
        return redirect('loginuser')

    prods_without_info = dict(request.POST)
    del prods_without_info['csrfmiddlewaretoken']

    cache.fs.save_foodmetric(prods_without_info)

    data = {'status': "инфа сохранена, круто!"}
    return JsonResponse(data, status=200)


def get_monthly_top(request):
    """выдает топ-10 продуктов месяца через ajax"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    if request.GET.get('client_id'):
        # если запрос от эксперта о клиенте
        client_id = request.GET.get('client_id')
        client = User.objects.get(id=client_id)
    else:
        # если запрос от самого клиента
        client = request.user

    month_str = request.GET.get('month')
    month_datetime = datetime.strptime(month_str, "%Y-%m")

    monthly_top = services.fs.monthly_top(client, month_datetime)

    return JsonResponse(monthly_top, status=200)
