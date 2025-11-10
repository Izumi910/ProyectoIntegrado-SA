from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Actualiza permisos del usuario administrador'

    def handle(self, *args, **options):
        try:
            # Buscar usuario admin
            admin = Usuario.objects.filter(rol='ADMINISTRADOR').first()
            if not admin:
                admin = Usuario.objects.filter(username='admin').first()
            
            if admin:
                # Aplicar todos los permisos
                admin.rol = 'ADMINISTRADOR'
                admin.puede_ver_usuarios = True
                admin.puede_crear_usuarios = True
                admin.puede_editar_usuarios = True
                admin.puede_eliminar_usuarios = True
                admin.puede_ver_productos = True
                admin.puede_crear_productos = True
                admin.puede_editar_productos = True
                admin.puede_eliminar_productos = True
                admin.puede_ver_proveedores = True
                admin.puede_crear_proveedores = True
                admin.puede_editar_proveedores = True
                admin.puede_eliminar_proveedores = True
                admin.puede_ver_inventario = True
                admin.puede_crear_inventario = True
                admin.puede_editar_inventario = True
                admin.puede_eliminar_inventario = True
                admin.puede_exportar_datos = True
                admin.puede_ver_reportes = True
                admin.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Permisos actualizados para {admin.username}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('No se encontró usuario administrador')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )