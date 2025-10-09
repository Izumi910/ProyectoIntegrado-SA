from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'marca', 'precio_venta', 'stock_minimo']
    search_fields = ['sku', 'nombre']
    list_filter = ['categoria', 'marca']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
