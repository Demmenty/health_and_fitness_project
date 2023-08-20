import json

from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from chat.forms import ChatMessageForm
from chat.models import ChatMessage


@login_required
@require_http_methods(["POST"])
def save_message(request):
    """Сохранение нового сообщения"""

    form = ChatMessageForm(request.POST, request.FILES)

    if form.is_valid():
        if not form.cleaned_data["text"] and not form.cleaned_data["image"]:
            return HttpResponseBadRequest("Необходимо передать text или image")

        message: ChatMessage = form.save()

        data = serialize("json", [message])
        return HttpResponse(data, content_type="application/json")

    data = {"error": form.errors}
    return JsonResponse(data, status=400)


@login_required
@require_http_methods(["POST"])
def make_message_read(request):
    """Сделать сообщение прочитанным"""

    message_id = request.POST.get("message_id")
    if not message_id:
        return HttpResponseBadRequest("Необходимо передать message_id")

    try:
        message = ChatMessage.objects.get(id=message_id)
    except ChatMessage.DoesNotExist:
        return HttpResponseBadRequest("Сообщение не найдено")

    message.is_read = True
    message.save()

    data = {"message_id": message_id}
    return JsonResponse(data, status=200)


@login_required
@require_http_methods(["GET"])
def get_message_by_id(request):
    """Получение сообщения по id"""

    message_id = request.GET.get("message_id")
    if not message_id:
        return HttpResponseBadRequest("Необходимо передать message_id")

    try:
        message = ChatMessage.objects.get(
            Q(sender=request.user) | Q(receiver=request.user), id=message_id
        )
    except ChatMessage.DoesNotExist:
        return HttpResponseBadRequest(
            "Сообщение не найдено или у вас нет прав"
        )

    data = serialize("json", [message])
    return HttpResponse(data, content_type="application/json")


@login_required
@require_http_methods(["POST"])
def get_msgs_list_by_id(request):
    """Получение списка сообщений по списку id"""

    message_id_list = request.POST.get("message_id_list")
    if not message_id_list:
        return HttpResponseBadRequest("Необходимо передать message_id_list")

    message_id_list = json.loads(message_id_list)
    if not isinstance(message_id_list, list):
        return HttpResponseBadRequest("message_id_list должен быть списком")

    messages = ChatMessage.objects.filter(id__in=message_id_list)
    return HttpResponse(
        serialize("json", messages), content_type="application/json"
    )


@login_required
@require_http_methods(["GET"])
def get_last_messages(request):
    """
    Получение списка последних сообщений (по возрастанию даты).
    Параметры фильтрации:
        participant - id участника диалога (для эксперта, необязательно)
        to_date - дата, до которой идет фильтрация сообщений (необязательно)
        limit - количество сообщений для выдачи (необязательно)
    """

    participant = request.GET.get("participant")
    to_date = request.GET.get("to_date")
    limit = request.GET.get("limit")

    if participant and request.user.is_expert:
        params = Q(sender=participant) | Q(receiver=participant)
    else:
        params = Q(sender=request.user) | Q(receiver=request.user)

    if to_date:
        params = params & Q(created_at__lte=parser.parse(to_date))

    if limit:
        messages = ChatMessage.objects.filter(params).order_by("-created_at")[
            : int(limit)
        ]
    else:
        messages = ChatMessage.objects.filter(params).order_by("-created_at")

    data = serialize("json", messages)
    return HttpResponse(data, content_type="application/json")


@login_required
@require_http_methods(["GET"])
def get_unread_messages(request):
    """
    Получение списка непрочитанных сообщений.
    Адресат - пользователь, сделавший запрос.
    Параметры фильтрации:
        sender - id отправителя (необязательно)
    """

    receiver = request.user
    sender = request.GET.get("sender")

    if sender:
        unread_messages = ChatMessage.objects.filter(
            sender=sender, receiver=receiver, is_read=False
        )
    else:
        unread_messages = ChatMessage.objects.filter(
            receiver=receiver, is_read=False
        )

    data = serialize("json", unread_messages)
    return HttpResponse(data, content_type="application/json")
