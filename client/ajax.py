from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from client.decorators import client_required
from client.forms import NoteForm
from client.models import Note


@client_required
@require_http_methods(["POST"])
def note_save(request):
    """Saves the client's personal note"""

    client = request.user
    note, _ = Note.objects.get_or_create(client=client)
    form = NoteForm(request.POST, instance=note)

    if form.is_valid():
        form.save()
        return HttpResponse("ok")

    return JsonResponse({"errors": form.errors}, status=400)
