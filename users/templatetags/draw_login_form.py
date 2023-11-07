from django import template

from users.forms import UserLoginForm

register = template.Library()


@register.inclusion_tag("users/login_form.html")
def draw_login_form() -> dict:
    """Draw login form"""

    data = {"login_form": UserLoginForm()}

    return data
