from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from consults.forms import NewRequestForm, RequestViewForm
from consults.models import Request
from expert.decorators import expert_required


@csrf_exempt
@require_http_methods(["POST"])
def save_new(request):
    """
    Saves new consultation requests from users.

    Parameters:
        request (HttpRequest): The object containing the POST data.

    Returns:
        HttpResponse: If the form is valid, returns an HTTP response with the message 'ok'.
        JsonResponse: If the form is invalid,
            returns a JSON response with the form errors and a status code of 400.
    """

    form = NewRequestForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponse("ok")

    return JsonResponse(form.errors, status=400)


@expert_required
@require_http_methods(["POST"])
def edit(request, id):
    """
    Saves changes made to a consultation request form.
    Used if the expert made changes or added a note to existing one.

    Parameters:
        request (HttpRequest): The object containing the POST data.
        id (int): The ID of the consultation request.

    Returns:
        HttpResponse: If the form is valid, returns an HTTP response with the message 'ok'.
        JsonResponse: If the form is invalid,
            returns a JSON response with the form errors and a status code of 400.
    """

    instance = get_object_or_404(Request, id=id)
    form = RequestViewForm(request.POST, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)


@expert_required
@require_http_methods(["POST"])
def set_seen(request, id):
    """
    Sets the 'seen' field of a consult request to True.

    Args:
        request: The HTTP request object (with request_id).
        id (int): The ID of the consultation request.

    Returns:
        HttpResponse: An HTTP response object with the message "ok".
    """

    instance = get_object_or_404(Request, id=id)

    instance.seen = True
    instance.save()

    return HttpResponse("ok")


@expert_required
@require_http_methods(["POST"])
def delete(request, id):
    """
    Deletes a consultation request.

    Args:
        request: The HTTP request object (with request_id).
        id (int): The ID of the consultation request.

    Returns:
        HttpResponse: An HTTP response object with the message "ok".
    """

    instance = get_object_or_404(Request, id=id)
    instance.delete()

    return HttpResponse("ok")
