from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from client_overview.forms import ClientContactForm, ClientMemoForm
from client_overview.models import ClientContact, ClientMemo


@login_required
@require_http_methods(["POST"])
def save_contacts(request):
    """сохраняет контакты клиента"""

    form = ClientContactForm(request.POST)

    if form.is_valid():
        instance, is_created = ClientContact.objects.get_or_create(
            user=request.user
        )
        form = ClientContactForm(request.POST, instance=instance)
        form.save()
        return HttpResponse("Контакты сохранены")
    else:
        return HttpResponseBadRequest("Ссылки введены некорректно. Попробуй ещё раз.")


@login_required
@require_http_methods(["POST"])
def save_clientmemo(request):
    """сохраняет личную заметку клиента"""

    form = ClientMemoForm(request.POST)

    if form.is_valid():
        instance = ClientMemo.objects.get(client=request.user)
        form = ClientMemoForm(request.POST, instance=instance)
        form.save()
        return HttpResponse("Ok")
    else:
        data = {"result": "Ошибка в полученных данных"}
        return JsonResponse(data, status=400)
