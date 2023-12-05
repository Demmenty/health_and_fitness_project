from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from expert.decorators import expert_required
from metrics.forms import LevelsForm
from metrics.models import Colors, Levels, PhotoAccess
from users.models import User


@login_required
@require_http_methods(["GET"])
def levels_colors_get(request):
    """
    Get the data for a colouring the client's metrics:
    parameters levels and colors which were set by the expert.

    Returns:
        JsonResponse: Response containing the data dictionary.
    """

    if request.user.is_expert:
        client = get_object_or_404(User, id=request.GET.get("client"))
    else:
        client = request.user

    colors = Colors.get_colors()
    levels = Levels.get_levels_as_dict(client=client)
    if not levels:
        return HttpResponseNotFound("Настройки не найдены")

    data = {
        "colors": colors,
        "parameters": levels,
    }
    return JsonResponse(data)


@expert_required
@require_http_methods(["POST"])
def levels_save(request, id: int):
    """
    Handles the saving of client metrics levels. Experts only.

    Args:
        request: HttpRequest object representing the incoming request.
        id: Integer representing the client ID.
    Returns:
        HttpResponse: Response indicating the success or failure of the operation.
    """

    client = get_object_or_404(User, id=id)
    form = LevelsForm(request.POST)

    if form.is_valid():
        parameter = form.cleaned_data["parameter"]
        instance = Levels.objects.filter(client=client, parameter=parameter).first()
        form = LevelsForm(request.POST, instance=instance)
        form.instance.client = client
        form.save()
        return HttpResponse(f'Измерения параметра "{parameter}" сохранены')

    return HttpResponseBadRequest("Данные некорректны")


@client_required
@require_http_methods(["POST"])
def photoaccess_edit(request):
    """
    Edit the access to clinet's anthropometry photos for the expert.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The response indicating the success of the operation.
    """

    is_allowed = request.POST.get("is_allowed") == "true"

    client = request.user
    instance, _ = PhotoAccess.objects.get_or_create(client=client)

    instance.is_allowed = is_allowed
    instance.save()

    return HttpResponse("ok")
