from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Actualiza el primer usuario a administrador'

    def handle(self, *args, **options):
        try:
            # Buscar el primer usuario o el superusuario
            usuario = Usuario.objects.filter(is_superuser=True).first()
            if not usuario:
                usuario = Usuario.objects.first()
            
            if usuario:
                usuario.rol = 'ADMINISTRADOR'
                usuario.save()
                self.stdout.write(f'Usuario {usuario.username} actualizado a ADMINISTRADOR')
            else:
                self.stdout.write('No se encontraron usuarios')
                
        except Exception as e:
            self.stdout.write(f'Error: {e}')