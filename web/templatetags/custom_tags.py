from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract arg from value."""
    return float(value) - float(arg)
