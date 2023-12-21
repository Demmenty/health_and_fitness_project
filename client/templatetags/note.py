from django import template

from client.forms import NoteForm
from client.models import Note

register = template.Library()


@register.inclusion_tag("client/note.html", takes_context=True)
def note(context) -> dict:
    """Renders the client's note"""

    client = context.request.user

    note, _ = Note.objects.get_or_create(client=client)
    form = NoteForm(instance=note)

    data = {"form": form}
    return data
