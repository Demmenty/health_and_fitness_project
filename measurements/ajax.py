from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from measurements.forms import AnthropometryPhotoAccessForm, MeasurementCommentForm, AnthropometryForm
from measurements.models import AnthropometryPhotoAccess, Measurement, Anthropometry
from .services import *
from measurements.utils import *


@login_required
@require_http_methods(["POST"])
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


@login_required
@require_http_methods(["GET"])
def get_color_settings(request):
    """Получение текущих настроек цветов показателей через ajax-запрос"""

    if request.GET.get("client_id"):
        # если запрос от эксперта о клиенте
        client_id = request.GET.get("client_id")
        client = User.objects.get(id=client_id)
    else:
        # если запрос от самого клиента
        client = request.user

    colorsettings = get_measurecolor_settings(client)

    return JsonResponse(colorsettings, status=200)


@login_required
@require_http_methods(["POST"])
def save_color_settings(request):
    """Сохранение настроек цветов для показателей клиента через ajax"""

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


@login_required
@require_http_methods(["POST"])
def photoaccess_change(request):
    """Обработка изменения настройки доступа к фото в антропометрии"""

    form = AnthropometryPhotoAccessForm(request.POST)

    if form.is_valid():

        instance = AnthropometryPhotoAccess.objects.get(user=request.user)
        form = AnthropometryPhotoAccessForm(request.POST, instance=instance)
        form.save()

        photoaccess_allowed = form.cleaned_data["photo_access"]
        if photoaccess_allowed:
            return HttpResponse("Доступ к фото разрешен")
        return HttpResponse("Доступ к фото запрещен")
    
    return HttpResponseBadRequest("Данные некорректны")


@login_required
@require_http_methods(["POST"])
def save_anthropometry(request):
    """Сохранение нового антропометрического измерения"""

    form = AnthropometryForm(request.POST, request.FILES)

    if form.is_valid():
        entry_date = form.cleaned_data["date"]
        instance = get_anthropo_entry(request.user, entry_date)

        if instance:
            form = AnthropometryForm(
                request.POST, request.FILES, instance=instance
            )
            form.save()
        else:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
        return HttpResponse("Измерения созранены")
    
    return HttpResponseBadRequest("Данные некорректны")
