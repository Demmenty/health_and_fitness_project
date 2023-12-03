from django import template
from django.template.context import RequestContext

from nutrition.forms import RecommendationForm
from nutrition.models import Recommendation

register = template.Library()


@register.inclusion_tag("nutrition/recommendations.html", takes_context=True)
def nutrition_recommendations(context: RequestContext) -> dict:
    """Renders the nutrition recommendations form for a client"""

    user = context.request.user
    client = context.get("client") if user.is_expert else user

    instance = Recommendation.objects.filter(client=client).first()
    form = RecommendationForm(instance=instance)

    data = {
        "user": user,
        "client": client,
        "form": form,
    }
    return data
