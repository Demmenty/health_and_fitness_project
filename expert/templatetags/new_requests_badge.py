from django import template

from consults.models import Request

register = template.Library()


@register.inclusion_tag("expert/new_requests_badge.html")
def new_requests_badge() -> dict:
    """Generates a badge for displaying the number of new consultation requests"""

    new_requests_count = Request.objects.filter(seen=False).count()

    data = {"new_requests_count": new_requests_count}
    return data
