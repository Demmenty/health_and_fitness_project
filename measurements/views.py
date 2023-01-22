from django.http import JsonResponse
from .services import *
from itertools import zip_longest
from django.contrib.auth.models import User


def get_color_settings(request):
    """Получение текущих настроек цветов показателей через ajax-запрос"""

    print('запрос get_color_settings получен')
    if request.user.is_anonymous:
        return JsonResponse({}, status=403)
    
    if request.GET.get('client_id'):
        # если запрос от эксперта о клиенте
        client_id = request.GET.get('client_id')
        client = User.objects.get(id=client_id)
    else:
        # если запрос от самого клиента
        client = request.user

    colorsettings = get_measurecolor_settings(client)

    return JsonResponse(colorsettings, status=200)


def save_color_settings(request):
    """Сохранение настроек цветов для показателей клиента через ajax"""
    if request.user.username != 'Parrabolla':
        data = {'status': 'No!'}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        # определение клиента
        client_id = request.POST.get('client_id')
        client = User.objects.get(id=client_id)
        # параметры цветовых настроек
        indices = request.POST.getlist('index')
        colors = request.POST.getlist('color')
        low_limits = request.POST.getlist('low_limit')
        up_limits = request.POST.getlist('upper_limit')
        # кулёк из параметров цветовых настроек
        colorset_values = zip_longest(indices, colors, low_limits, up_limits)

        save_measurecolor_settings(client, colorset_values)

        data = {}
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

    monthly_top = create_monthly_top(client, month_datetime)

    return JsonResponse(monthly_top, status=200)
    
