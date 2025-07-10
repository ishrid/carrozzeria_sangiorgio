# main/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def splitlines(value):
    """
    Splits a string by newline characters and returns a list of stripped strings.
    Handles non-string inputs gracefully.
    """
    if value is None:
        return [] # Return an empty list if value is None
    if not isinstance(value, str):
        # Convert to string and then process, or handle as needed
        value = str(value)

    # Split by lines, and then strip whitespace from EACH line
    return [line.strip() for line in value.splitlines()]