from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from expert.decorators import expert_required
from expert.forms import ClientMainNoteForm, ClientMonthlyNoteForm
from expert.models import ClientMainNote, ClientMonthlyNote


@expert_required
@require_http_methods(["POST"])
def main_note_save(request):
    """Saves the expert's main note about a client"""

    client_id = request.POST.get("client")
    note, _ = ClientMainNote.objects.get_or_create(client_id=client_id)
    form = ClientMainNoteForm(request.POST, instance=note)

    if form.is_valid():
        form.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)


@expert_required
@require_http_methods(["GET"])
def monthly_note_get(request):
    """Retrieves an expert's monthly note about a client for the specific month"""

    client_id = request.GET.get("client_id")
    month = request.GET.get("month")
    year = request.GET.get("year")

    note = ClientMonthlyNote.objects.filter(
        client_id=client_id, month=month, year=year
    ).first()

    data = model_to_dict(note) if note else {}
    return JsonResponse(data)


@expert_required
@require_http_methods(["POST"])
def monthly_note_save(request):
    """Saves the monthly expert's note about a client"""

    client_id = request.POST.get("client")
    month = request.POST.get("month")
    year = request.POST.get("year")

    instance = ClientMonthlyNote.objects.filter(
        client_id=client_id, month=month, year=year
    ).first()
    form = ClientMonthlyNoteForm(request.POST, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)
