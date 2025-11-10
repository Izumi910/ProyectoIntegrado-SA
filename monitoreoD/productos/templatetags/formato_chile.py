from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def formato_precio(value):
    """Formatea precios para Chile: sin decimales si es entero, con decimales si es necesario"""
    if value is None:
        return '0'
    
    try:
        decimal_value = Decimal(str(value))
        # Si es un número entero, mostrar sin decimales
        if decimal_value == decimal_value.to_integral_value():
            return f"{int(decimal_value):,}".replace(',', '.')
        # Si tiene decimales, mostrar máximo 2 decimales
        else:
            formatted = f"{decimal_value:.2f}".rstrip('0').rstrip('.')
            # Formatear con separadores de miles
            parts = formatted.split('.')
            parts[0] = f"{int(parts[0]):,}".replace(',', '.')
            return '.'.join(parts) if len(parts) > 1 else parts[0]
    except:
        return str(value)

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