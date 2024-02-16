from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from chat.forms import MessageForm
from chat.models import Message
from users.models import EXPERT


@login_required
@require_http_methods(["POST"])
def save_msg(request):
    """
    Saves a chat message sent via a POST request.

    Parameters:
        request (HttpRequest): The object containing the POST data.

    Returns:
        HttpResponse or JsonResponse: The HttpResponse object with the serialized message data in JSON format.
        If the form is not valid, returns a JsonResponse object with the form errors and a status code of 400.
    """

    form = MessageForm(request.POST, request.FILES)

    if form.is_valid():
        message: Message = form.save()
        data = serialize("json", [message])
        return HttpResponse(data, content_type="application/json")

    return JsonResponse({"errors": form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def set_seen(request):
    """
    Sets the 'seen' attribute of a message to True.

    Args:
        request: The HTTP request object (with message_id).

    Returns:
        HttpResponse: A response object with the string "ok".
    """

    message_id = request.POST.get("message_id")
    message = get_object_or_404(Message, pk=message_id)

    message.seen = True
    message.save()

    return HttpResponse("ok")


@login_required
@require_http_methods(["POST"])
def delete_msg(request):
    """
    Deletes a message.

    Args:
        request: The HTTP request object (with message_id).

    Returns:
        HttpResponse: A response object with the string "ok".
    """

    message_id = request.POST.get("message_id")
    message = get_object_or_404(Message, pk=message_id)

    if message.sender != request.user:
        return HttpResponseForbidden("Недостаточно прав!")

    message.delete()

    return HttpResponse("ok")


@login_required
@require_http_methods(["GET"])
def get_last_msgs(request):
    """
    Retrieves last chat messages between client and expert.

    Args:
        request (HttpRequest): The object containing the GET parameters:
            partner_id (int): The ID of another chat participant.
                Mandatory if the user is an expert (to identify the client).
            limit (int): The maximum number of messages to retrieve. Defaults to 10.

    Returns:
        HttpResponse: The JSON response containing the serialized messages.
    """

    limit = int(request.GET.get("limit", 10))

    user = request.user
    partner_id = request.GET.get("partner_id") if user.is_expert else EXPERT.id

    messages = Message.objects.filter_by_participants(user.id, partner_id)
    last_messages = messages.order_by("-created_at")[:limit]

    data = serialize("json", last_messages)
    return HttpResponse(data, content_type="application/json")


@login_required
@require_http_methods(["GET"])
def get_old_msgs(request):
    """
    Retrieves chat messages older than message with the provided ID.

    Args:
        request (HttpRequest): The object containing the GET parameters:
            partner_id (int): The ID of another chat participant.
                Mandatory if the user is an expert (to identify the client).
            message_id (int): The ID of the message to retrieve older messages from.
            limit (int): The maximum number of messages to retrieve. Defaults to 10.

    Returns:
        HttpResponse: The JSON response containing the serialized messages.
    """

    message_id = request.GET.get("message_id")
    if not message_id:
        return HttpResponseBadRequest(
            "message_id to retrieve older messages from is required"
        )

    limit = int(request.GET.get("limit", 10))

    user = request.user
    partner_id = request.GET.get("partner_id") if user.is_expert else EXPERT.id

    messages = Message.objects.filter_by_participants(user.id, partner_id)
    older_msgs = messages.filter(id__lt=message_id).order_by("-created_at")[:limit]

    data = serialize("json", older_msgs)
    return HttpResponse(data, content_type="application/json")


@login_required
@require_http_methods(["GET"])
def get_new_msgs(request):
    """
    Retrieves new chat messages after message with the provided ID.

    Args:
        request (HttpRequest): The object containing the GET parameters:
            partner_id (int): The ID of the other chat participant.
                Mandatory if the user is an expert (to identify the client).
            message_id (int): The ID of the message to retrieve newer messages from.
                If not provided, retrieves all messages.

    Returns:
        HttpResponse: The JSON response containing the serialized messages.
    """

    user = request.user
    partner_id = request.GET.get("partner_id") if user.is_expert else EXPERT.id
    messages = Message.objects.filter_by_participants(user.id, partner_id).order_by(
        "created_at"
    )

    message_id = request.GET.get("message_id")
    if message_id:
        messages = messages.filter(id__gt=message_id).order_by("created_at")

    data = serialize("json", messages)
    return HttpResponse(data, content_type="application/json")


@login_required
@require_http_methods(["GET"])
def count_new_msgs(request):
    """
    Retrieves the amount of new messages.
    New messages are messages that have been sent by the chat partner
    to the user but have not been seen by him.

    Args:
        request (HttpRequest): The object containing the GET parameters:
            partner_id (int): The ID of the chat partner.
                Mandatory if the user is an expert (to identify the client).

    Returns:
        JsonResponse: A JSON response containing the amount of new messages.
    """

    user = request.user
    partner_id = request.GET.get("partner_id") if user.is_expert else EXPERT.id

    new_msgs = Message.objects.filter(sender_id=partner_id, recipient=user, seen=False)

    return JsonResponse({"count": new_msgs.count()})
