from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Prueba el envío de emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Email de destino'
        )

    def handle(self, *args, **options):
        destinatario = options['to']
        
        self.stdout.write(self.style.WARNING(f'Enviando email de prueba a {destinatario}...'))
        self.stdout.write(f'Backend: {settings.EMAIL_BACKEND}')
        
        try:
            send_mail(
                subject='Prueba de Email - Lilis Dulcería',
                message='Este es un email de prueba desde el sistema de Lilis Dulcería.\n\nSi recibes este mensaje, la configuración de email está funcionando correctamente.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Email enviado exitosamente a {destinatario}!')
            )
            self.stdout.write('Revisa tu bandeja de entrada (y spam).')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al enviar email: {str(e)}')
            )
            self.stdout.write('\nVerifica tu configuración en .env:')
            self.stdout.write('- EMAIL_USE_REAL=True')
            self.stdout.write('- EMAIL_HOST_USER=tu_email@gmail.com')
            self.stdout.write('- EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación')
