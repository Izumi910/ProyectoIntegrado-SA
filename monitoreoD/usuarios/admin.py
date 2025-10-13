from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'is_staff', 'mostrar_grupos', 'estado', 'ultimo_acceso']
    search_fields = ['username', 'email']
    list_filter = ['estado']

    def mostrar_grupos(self, obj):
        return ", ".join([g.name for g in obj.groups.all()]) if obj.groups.exists() else "-"
    mostrar_grupos.short_description = 'Groups'