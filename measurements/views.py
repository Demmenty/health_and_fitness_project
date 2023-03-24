from itertools import zip_longest

from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import MeasurementCommentForm
from .models import Measurement
from .services import *


def save_measure_comment(request):
    """Сохранение коммента к измерениям показателей через ajax"""
    # получаем форму из запроса
    form = MeasurementCommentForm(request.POST)
    # проверяем на корректность
    if form.is_valid():
        # получаем дату из формы
        comment_date = form.cleaned_data["date"]
        # получаем запись из БД с этим числом
        measure = Measurement.objects.get(date=comment_date, user=request.user)
        # перезаписываем
        form = MeasurementCommentForm(request.POST, instance=measure)
        form.save()
        new_comment = form.cleaned_data["comment"]
        data = {
            "new_comment": new_comment,
        }
        return JsonResponse(data, status=200)


def get_color_settings(request):
    """Получение текущих настроек цветов показателей через ajax-запрос"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    if request.GET.get("client_id"):
        # если запрос от эксперта о клиенте
        client_id = request.GET.get("client_id")
        client = User.objects.get(id=client_id)
    else:
        # если запрос от самого клиента
        client = request.user

    colorsettings = get_measurecolor_settings(client)

    return JsonResponse(colorsettings, status=200)


def save_color_settings(request):
    """Сохранение настроек цветов для показателей клиента через ajax"""

    if request.user.username != "Parrabolla":
        return JsonResponse({}, status=403)

    if request.method == "POST":
        # определение клиента
        client_id = request.POST.get("client_id")
        client = User.objects.get(id=client_id)

        # параметры цветовых настроек
        indices = request.POST.getlist("index")
        colors = request.POST.getlist("color")
        low_limits = request.POST.getlist("low_limit")
        up_limits = request.POST.getlist("upper_limit")
        # кулёк из параметров цветовых настроек
        colorset_values = zip_longest(indices, colors, low_limits, up_limits)

        save_measeurecolor_settings(client, colorset_values)

        return JsonResponse({}, status=200)
