from django import template

register = template.Library()

@register.filter
def times(number):
    """Returns a range from 0 to number-1"""
    return range(number)

