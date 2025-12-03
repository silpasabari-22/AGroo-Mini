from django import template

register = template.Library()

@register.filter
def multiply(q, p):
    try:
        return float(q) * float(p)
    except:
        return 0
