from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from .forms import ClientContactForm, ClientMemoForm
from .models import ClientContact, ClientMemo


def save_contacts(request):
    """сохраняет контакты клиента"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    form = ClientContactForm(request.POST)

    if form.is_valid():
        instance, is_created = ClientContact.objects.get_or_create(
            user=request.user
        )
        form = ClientContactForm(request.POST, instance=instance)
        form.save()

        data = {"result": "Контакты сохранены"}
        return JsonResponse(data, status=200)

    else:
        data = {"result": "Ссылки введены некорректно. Попробуйте ещё раз."}
        return JsonResponse(data, status=200)


def save_clientmemo(request):
    """сохраняет личную заметку клиента"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    form = ClientMemoForm(request.POST)

    if form.is_valid():
        instance = ClientMemo.objects.get(client=request.user)
        form = ClientMemoForm(request.POST, instance=instance)
        form.save()
        return HttpResponse("Ok")
    else:
        data = {"result": "Ошибка в полученных данных"}
        return JsonResponse(data, status=400)
