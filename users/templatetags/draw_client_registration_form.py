from django import template

from users.forms import ClientRegistrationForm

register = template.Library()


@register.inclusion_tag("users/client_registration_form.html")
def draw_client_registration_form() -> dict:
    """Draw client registration form"""

    data = {"client_registration_form": ClientRegistrationForm()}

    return data
