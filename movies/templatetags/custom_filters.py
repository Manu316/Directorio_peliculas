from django import template
from datetime import date

register = template.Library()

@register.filter(name='add')
def add(value, arg):
    """Adds the argument (string) to the value (string). Used for poster paths."""
    try:
        return str(value) + str(arg)
    except Exception:
        return ''

@register.filter(name='split')
def split(value, key):
    """Returns the first part of a string split by a key (e.g., gets '2024' from '2024-05-15')."""
    if isinstance(value, str) and key in value:
        return value.split(key)[0]
    return value
    
@register.filter(name='is_date_string')
def is_date_string(value):
    """Checks if the value is a non-empty string."""
    return isinstance(value, str) and value != ''