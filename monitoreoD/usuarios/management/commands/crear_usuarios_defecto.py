from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea usuarios por defecto con diferentes roles'

    def handle(self, *args, **options):
        # Administrador
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_user(
                username='admin',
                email='admin@lilis.com',
                password='Admin123',
                first_name='Administrador',
                last_name='Sistema',
                rol='ADMINISTRADOR',
                area='Administración'
            )
            self.stdout.write(f'Usuario administrador creado: {admin.username}')

        # Editor
        if not Usuario.objects.filter(username='editor').exists():
            editor = Usuario.objects.create_user(
                username='editor',
                email='editor@lilis.com',
                password='Editor123',
                first_name='Editor',
                last_name='Contenido',
                rol='EDITOR',
                area='Ventas'
            )
            self.stdout.write(f'Usuario editor creado: {editor.username}')

        # Lector
        if not Usuario.objects.filter(username='lector').exists():
            lector = Usuario.objects.create_user(
                username='lector',
                email='lector@lilis.com',
                password='Lector123',
                first_name='Lector',
                last_name='Consulta',
                rol='LECTOR',
                area='Consultas'
            )
            self.stdout.write(f'Usuario lector creado: {lector.username}')

        self.stdout.write(self.style.SUCCESS('Usuarios por defecto creados exitosamente'))