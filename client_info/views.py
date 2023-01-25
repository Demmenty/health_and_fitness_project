from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ClientContactForm, HealthQuestionaryForm
from .models import ClientContact, HealthQuestionary


def save_contacts(request):
    """сохраняет контакты клиента"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    form = ClientContactForm(request.POST)

    if form.is_valid():
        instance, is_created = ClientContact.objects.get_or_create(user=request.user)
        form = ClientContactForm(request.POST, instance=instance)
        form.save()

        data = {'result': 'Контакты сохранены'}
        return JsonResponse(data, status=200)

    else:

        data = {'result': 'Ссылки введены некорректно. Попробуйте ещё раз.'}
        return JsonResponse(data, status=200)


