from django import template

register = template.Library()

@register.filter
def multiply(a, b):
    try:
        return float(a) * float(b)
    except:
        return 0

@register.filter
def divide(a, b):
    try:
        return float(a) / float(b)
    except:
        return 0
