import typing
from urllib.parse import urlencode

from django.shortcuts import redirect
from django.urls import reverse

if typing.TYPE_CHECKING:
    from training.models import Training


def redirect_to_training(training: "Training"):
    """
    Redirects the user to the training page for a specific training.

    Args:
        training (Training): The training object.
    """

    params = {
        "client_id": training.client.id,
        "day": training.date,
    }
    training_page = f"{reverse('training:trainings')}?{urlencode(params)}"
    return redirect(training_page)
