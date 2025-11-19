from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Limpia sesiones expiradas de la base de datos'

    def handle(self, *args, **options):
        # Eliminar sesiones expiradas
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Se eliminaron {count} sesiones expiradas')
        )
