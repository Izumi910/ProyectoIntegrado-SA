from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Obtiene un atributo de un objeto"""
    return getattr(obj, attr, False)