from django.forms import ModelForm

from client.models import Log
from users.models import User


def create_log_entry(
    modelname: str, description: str, client: User, link: str = None
) -> None:
    """
    Save a log entry about client activity with the given description.

    Args:
        modelname (str): The name of the model changed.
        description (str): The change message.
        client (User): The client object.
        link (str, optional): The link to look at the changed object.
    """

    Log.objects.create(
        modelname=modelname,
        description=description,
        client=client,
        link=link,
    )


def create_change_log_entry(form: ModelForm, client: User, link: str = None) -> None:
    """
    Creates a log entry for the changes made in the form if any.

    Args:
        form (ModelForm): The form containing the changed data.
        client (User): The user making the changes.
        link (str, optional): The link to look at the changed object.
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
    modelname = form.Meta.model._meta.verbose_name

    create_log_entry(modelname, description, client, link)
