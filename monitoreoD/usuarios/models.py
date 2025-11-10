from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

def user_avatar_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'

class Usuario(AbstractUser):
    ROLES = [
        ('ADMINISTRADOR', 'Administrador del Sistema'),
        ('GERENTE_GENERAL', 'Gerente General'),
        ('GERENTE_INVENTARIO', 'Gerente de Inventario'),
        ('GERENTE_VENTAS', 'Gerente de Ventas'),
        ('SUPERVISOR_INVENTARIO', 'Supervisor de Inventario'),
        ('OPERADOR_INVENTARIO', 'Operador de Inventario'),
        ('VENDEDOR', 'Vendedor'),
        ('CONTADOR', 'Contador'),
        ('LECTOR', 'Solo Lectura'),
    ]
    
    telefono = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=20, default="ACTIVO")
    mfa_habilitado = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    rol = models.CharField(max_length=30, choices=ROLES, default='LECTOR')
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='Imagen de perfil (JPG, JPEG, PNG - máximo 2MB)'
    )
    
    # Permisos granulares personalizables
    puede_ver_usuarios = models.BooleanField(default=False)
    puede_crear_usuarios = models.BooleanField(default=False)
    puede_editar_usuarios = models.BooleanField(default=False)
    puede_desactivar_usuarios = models.BooleanField(default=False)
    
    puede_ver_productos = models.BooleanField(default=True)
    puede_crear_productos = models.BooleanField(default=False)
    puede_editar_productos = models.BooleanField(default=False)
    puede_desactivar_productos = models.BooleanField(default=False)
    
    puede_ver_proveedores = models.BooleanField(default=True)
    puede_crear_proveedores = models.BooleanField(default=False)
    puede_editar_proveedores = models.BooleanField(default=False)
    puede_desactivar_proveedores = models.BooleanField(default=False)
    
    puede_ver_inventario = models.BooleanField(default=True)
    puede_crear_inventario = models.BooleanField(default=False)
    puede_editar_inventario = models.BooleanField(default=False)
    
    puede_exportar_usuarios = models.BooleanField(default=False)
    puede_exportar_productos = models.BooleanField(default=False)
    puede_exportar_proveedores = models.BooleanField(default=False)
    puede_exportar_inventario = models.BooleanField(default=False)
    puede_ver_reportes = models.BooleanField(default=False)
    
    def aplicar_permisos_por_rol(self):
        """Aplica permisos predeterminados basados en el rol"""
        if self.rol == 'ADMINISTRADOR':
            self.puede_ver_usuarios = True
            self.puede_crear_usuarios = True
            self.puede_editar_usuarios = True
            self.puede_desactivar_usuarios = True
            self.puede_ver_productos = True
            self.puede_crear_productos = True
            self.puede_editar_productos = True
            self.puede_desactivar_productos = True
            self.puede_ver_proveedores = True
            self.puede_crear_proveedores = True
            self.puede_editar_proveedores = True
            self.puede_desactivar_proveedores = True
            self.puede_ver_inventario = True
            self.puede_crear_inventario = True
            self.puede_editar_inventario = True
            self.puede_exportar_usuarios = True
            self.puede_exportar_productos = True
            self.puede_exportar_proveedores = True
            self.puede_exportar_inventario = True
            self.puede_ver_reportes = True
        elif 'GERENTE' in self.rol:
            self.puede_ver_usuarios = False
            self.puede_crear_usuarios = False
            self.puede_editar_usuarios = False
            self.puede_desactivar_usuarios = False
            self.puede_ver_productos = True
            self.puede_crear_productos = True
            self.puede_editar_productos = True
            self.puede_desactivar_productos = False
            self.puede_ver_proveedores = True
            self.puede_crear_proveedores = True
            self.puede_editar_proveedores = True
            self.puede_desactivar_proveedores = False
            self.puede_ver_inventario = True
            self.puede_crear_inventario = True
            self.puede_editar_inventario = True
            self.puede_exportar_usuarios = False
            self.puede_exportar_productos = True
            self.puede_exportar_proveedores = True
            self.puede_exportar_inventario = True
            self.puede_ver_reportes = True
        elif 'SUPERVISOR' in self.rol:
            self.puede_ver_usuarios = False
            self.puede_crear_usuarios = False
            self.puede_editar_usuarios = False
            self.puede_desactivar_usuarios = False
            self.puede_ver_productos = True
            self.puede_crear_productos = True
            self.puede_editar_productos = True
            self.puede_desactivar_productos = False
            self.puede_ver_proveedores = True
            self.puede_crear_proveedores = False
            self.puede_editar_proveedores = False
            self.puede_desactivar_proveedores = False
            self.puede_ver_inventario = True
            self.puede_crear_inventario = True
            self.puede_editar_inventario = True
            self.puede_exportar_usuarios = False
            self.puede_exportar_productos = False
            self.puede_exportar_proveedores = False
            self.puede_exportar_inventario = True
            self.puede_ver_reportes = False
        else:  # OPERADOR, VENDEDOR, CONTADOR, LECTOR
            self.puede_ver_usuarios = False
            self.puede_crear_usuarios = False
            self.puede_editar_usuarios = False
            self.puede_desactivar_usuarios = False
            self.puede_ver_productos = True
            self.puede_crear_productos = False
            self.puede_editar_productos = False
            self.puede_desactivar_productos = False
            self.puede_ver_proveedores = False
            self.puede_crear_proveedores = False
            self.puede_editar_proveedores = False
            self.puede_desactivar_proveedores = False
            self.puede_ver_inventario = True
            self.puede_crear_inventario = False
            self.puede_editar_inventario = False
            self.puede_exportar_usuarios = False
            self.puede_exportar_productos = False
            self.puede_exportar_proveedores = False
            self.puede_exportar_inventario = False
            self.puede_ver_reportes = False
    
    # Métodos de permisos simplificados
    def puede_gestionar_usuarios(self):
        if self.rol == 'ADMINISTRADOR':
            return True
        return self.puede_ver_usuarios
    
    def save(self, *args, **kwargs):
        # Aplicar permisos automáticamente al guardar
        if self.pk is None or 'rol' in kwargs.get('update_fields', []):
            self.aplicar_permisos_por_rol()
        super().save(*args, **kwargs)

