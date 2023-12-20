from datetime import date

from django import template

from expert.forms import ClientMainNoteForm, ClientMonthlyNoteForm
from expert.models import ClientMainNote, ClientMonthlyNote

register = template.Library()


@register.inclusion_tag("expert/notes.html", takes_context=True)
def expert_notes(context) -> dict:
    """Renders the notes about specific client for expert"""

    client = context["client"]
    today = date.today()
    month = today.month
    year = today.year

    main_note, _ = ClientMainNote.objects.get_or_create(client=client)
    monthly_note = ClientMonthlyNote.objects.filter(
        client=client, month=month, year=year
    ).first()

    main_note_form = ClientMainNoteForm(instance=main_note)
    monthly_note_form = ClientMonthlyNoteForm(
        instance=monthly_note,
        initial={"client": client, "month": month, "year": year},
    )

    data = {
        "client": client,
        "main_note_form": main_note_form,
        "monthly_note_form": monthly_note_form,
    }
    return data
