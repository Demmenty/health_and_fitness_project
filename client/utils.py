from django.forms import ModelForm

from client.models import Log
from users.models import User


def create_log_entry(form: ModelForm, description: str, client: User) -> None:
    """
    Save a log entry for a model form about client activity
    with the given description.

    Args:
        form (ModelForm): The model form object.
        description (str): The change message.
        client (User): The client object.
    """

    Log.objects.create(
        modelname=form.Meta.model._meta.verbose_name,
        description=description,
        client=client,
    )


def create_change_log_entry(form: ModelForm, client: User) -> None:
    """
    Creates a log entry for the changes made in the form if any.

    Args:
        form (ModelForm): The form containing the changed data.
        client (User): The user making the changes.
    """

    if not form.has_changed():
        return

    changed_fields_verbose_names = []
    for field_name in form.changed_data:
        field = form.fields[field_name]
        verbose_name = field.label if field.label else field_name.replace("_", " ")
        verbose_name = f'"{str(verbose_name).lower()}"'
        changed_fields_verbose_names.append(verbose_name)

    changed_fields_description = ", ".join(changed_fields_verbose_names)
    description = f"Изменения: {changed_fields_description}"
    create_log_entry(form, description, client)
