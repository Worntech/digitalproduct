from django import template

register = template.Library()

@register.filter
def to(value):
    """Returns a list of numbers from 1 to value."""
    return range(1, value + 1)
