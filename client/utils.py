from django.forms import ModelForm

from client.models import Log
from users.models import User

# TODO rename this file to log_utils.py or smth


def create_log_entry(form: ModelForm, change_message: str, client: User) -> None:
    """
    Save a log entry for a model form about client activity.

    Args:
        form (ModelForm): The model form object.
        change_message (str): The change message.
        client (User): The client object.
    """

    Log.objects.create(
        modelname=form.Meta.model.__name__,
        change_message=change_message[:255],
        client=client,
    )


def create_change_log_entry(form: ModelForm, client: User) -> None:
    """
    Creates a log entry for the changes made in the form.

    Args:
        form (ModelForm): The form containing the changed data.
        client (User): The user making the changes.
    """
    if form.changed_data:
        changed_fields = ", ".join(form.changed_data)
        change_message = f"Изменены поля: {changed_fields}"
        create_log_entry(form, change_message, client)
