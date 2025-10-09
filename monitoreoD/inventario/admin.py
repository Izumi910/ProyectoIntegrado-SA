from django.contrib import admin
from .models import MovimientoInventario

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'tipo', 'producto', 'proveedor', 'cantidad']
    search_fields = ['producto__nombre']
    list_filter = ['tipo', 'producto']