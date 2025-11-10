from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def formato_cantidad(value):
    """Formatea cantidades: sin decimales si es entero"""
    if value is None:
        return '0'
    
    try:
        decimal_value = Decimal(str(value))
        # Si es un número entero, mostrar sin decimales
        if decimal_value == decimal_value.to_integral_value():
            return str(int(decimal_value))
        # Si tiene decimales, mostrar máximo 2 decimales
        else:
            return f"{decimal_value:.2f}".rstrip('0').rstrip('.')
    except:
        return str(value)