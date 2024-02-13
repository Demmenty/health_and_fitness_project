import re
import types
from copy import copy

from django.template import Library

from main.utils import get_noun_ending

register = Library()


@register.filter("add_ending")
def add_ending(number: int, endings: str):
    """
    A function that adds an appropriate ending to a given number
    based on a list of endings.
    If the number is a string, it will return it.

    Example: add_ending(4, 'слон', 'слона', 'слонов') --> '4 слона'

    Args:
        number (int): The number to which the ending will be added.
        endings (str): A comma-separated list of possible endings:
            first (str) - The noun ending for numbers ending in 1.
            second (str) - The noun ending for numbers ending in 2, 3, or 4.
            third (str) - The noun ending for numbers ending in 0 or 5-9.

    Returns:
        str: The original number with the appropriate ending added.
    """

    if isinstance(number, str):
        return number

    return f'{number} {get_noun_ending(number, *endings.split(","))}'


def silence_without_field(fn):
    def wrapped(field, attr):
        if not field:
            return ""
        return fn(field, attr)

    return wrapped


def _process_field_attributes(field, attr, process):
    params = re.split(r"(?<!:):(?!:)", attr, 1)
    attribute = params[0].replace("::", ":")
    value = params[1] if len(params) == 2 else True
    field = copy(field)
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        if attribute == "type":  # change the Input type
            self.field.widget.input_type = value
            del attrs["type"]
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += " " + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + " " + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("add_class")
@silence_without_field
def add_class(field, css_class):
    return append_attr(field, "class:" + css_class)


@register.filter("remove_attr")
@silence_without_field
def remove_attr(field, attr):
    if attr in field.field.widget.attrs:
        del field.field.widget.attrs[attr]
    return field


@register.filter("get_value")
def get_value(dictionary, key):
    return dictionary.get(key, "")


@register.filter("multiply")
def multiply(field, num):
    if field and num:
        return field * num
