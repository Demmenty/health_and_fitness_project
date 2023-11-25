from django import template
from django.template.context import RequestContext

from metrics.forms import NutritionRecsForm
from metrics.models import NutritionRecs

register = template.Library()

# TODO replace nutricion recs to nutrition module


@register.inclusion_tag("nutrition/recommendations.html", takes_context=True)
def nutrition_recommendations(context: RequestContext) -> dict:
    """Renders the nutrition recommendations form for a client"""

    user = context.request.user
    client = context.get("client") if user.is_expert else user

    instance = NutritionRecs.objects.filter(client=client).first()
    form = NutritionRecsForm(instance=instance)

    data = {
        "user": user,
        "client": client,
        "form": form,
    }
    return data
