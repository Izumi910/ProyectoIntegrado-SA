from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'estado', 'ultimo_acceso']
    search_fields = ['username', 'email']
    list_filter = ['estado']