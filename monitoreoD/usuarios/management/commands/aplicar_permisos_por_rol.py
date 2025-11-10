from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Aplica permisos por defecto a todos los usuarios según su rol'

    def handle(self, *args, **options):
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            usuario.aplicar_permisos_por_rol()
            usuario.save()
            self.stdout.write(
                self.style.SUCCESS(f'Permisos aplicados para {usuario.username} ({usuario.get_rol_display()})')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Permisos aplicados exitosamente a {usuarios.count()} usuarios')
        )