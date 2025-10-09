from django.contrib import admin
from .models import Proveedor, ProveedorProducto

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'rut_nif', 'email', 'telefono', 'estado']
    search_fields = ['razon_social', 'rut_nif', 'email']
    list_filter = ['estado']

@admin.register(ProveedorProducto)
class ProveedorProductoAdmin(admin.ModelAdmin):
    list_display = ['proveedor', 'producto', 'costo', 'lead_time_dias', 'preferente']
    search_fields = ['proveedor__razon_social', 'producto__nombre']
    list_filter = ['preferente']