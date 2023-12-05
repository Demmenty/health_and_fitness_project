from metrics.forms import LevelsForm
from metrics.models import Daily as DailyMetrics, Levels
from users.models import User


def create_levels_forms(client: User) -> list[LevelsForm]:
    """
    Generate a list of metrics LevelsForm based on the client
    for each metric parameter in DailyMetrics.

    Args:
        client (User): The user client.
    Returns:
        list[LevelsForm]: A list of LevelsForm objects.
    """

    levels_forms = []
    instances = Levels.objects.filter(client=client)

    for parameter in DailyMetrics.Parameters:
        instance = instances.filter(parameter=parameter).first()
        if instance:
            form = LevelsForm(instance=instance)
        else:
            form = LevelsForm(initial={"client": client, "parameter": parameter})
        levels_forms.append(form)

    return levels_forms
