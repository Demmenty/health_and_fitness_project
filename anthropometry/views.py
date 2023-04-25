from django.http import JsonResponse
from django.shortcuts import render

from .forms import AnthropometryPhotoAccessForm
from .models import Anthropometry, AnthropometryPhotoAccess


# Create your views here.
def photoaccess_change(request):
    """Обработка изменения настройки доступа к фото в антропометрии"""
    # получаем форму из запроса
    form = AnthropometryPhotoAccessForm(request.POST)
    # проверяем на корректность
    if form.is_valid():
        # записываем значение в базу
        instance = AnthropometryPhotoAccess.objects.get(user=request.user)
        form = AnthropometryPhotoAccessForm(request.POST, instance=instance)
        form.save()

        photoaccess_allowed = form.cleaned_data["photo_access"]
        data = {
            "photoaccess_allowed": photoaccess_allowed,
        }
        return JsonResponse(data, status=200)
