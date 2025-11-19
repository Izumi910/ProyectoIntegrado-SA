import logging
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger('django')

class EmailService:
    @staticmethod
    def generate_secure_password(length=12):
        """Genera contraseña segura aleatoria"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        # Asegurar requisitos mínimos
        if not any(c.isupper() for c in password):
            password = password[:-1] + secrets.choice(string.ascii_uppercase)
        if not any(c.islower() for c in password):
            password = password[:-1] + secrets.choice(string.ascii_lowercase)
        if not any(c.isdigit() for c in password):
            password = password[:-1] + secrets.choice(string.digits)
            
        return password

    @staticmethod
    def send_new_user_email(user, password):
        """Envía email con contraseña a usuario nuevo"""
        try:
            subject = 'Bienvenido a Lilis - Tu cuenta ha sido creada'
            
            message = f"""
Hola {user.get_full_name() or user.username},

¡Bienvenido a Lilis Dulcería!

Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales de acceso:

Usuario: {user.username}
Contraseña temporal: {password}
Email: {user.email}

⚠️ IMPORTANTE: Por tu seguridad, debes cambiar esta contraseña en tu primer inicio de sesión.

Enlace de acceso: http://127.0.0.1:8080/usuarios/login/

Si tienes alguna pregunta, contacta a: {settings.DEFAULT_FROM_EMAIL}

Saludos,
Equipo de Lilis Dulcería
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f'Email de bienvenida enviado a {user.email}')
            return True
            
        except Exception as e:
            logger.error(f'Error enviando email a {user.email}: {str(e)}')
            return False

    @staticmethod
    def send_password_changed_email(user):
        """Envía email cuando se cambia la contraseña"""
        try:
            subject = 'Contraseña cambiada - Lilis Dulcería'
            
            message = f"""
Hola {user.get_full_name() or user.username},

Te informamos que tu contraseña ha sido cambiada exitosamente.

Detalles del cambio:
- Fecha y hora: {timezone.now().strftime('%d/%m/%Y a las %H:%M')}
- Usuario: {user.username}

🚨 Si NO fuiste tú quien realizó este cambio, contacta inmediatamente a: {settings.DEFAULT_FROM_EMAIL}

Recomendaciones de seguridad:
- Revisa tu cuenta regularmente
- No compartas tus credenciales
- Usa contraseñas seguras y únicas

Saludos,
Equipo de Lilis Dulcería
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f'Email de cambio de contraseña enviado a {user.email}')
            return True
            
        except Exception as e:
            logger.error(f'Error enviando email de cambio de contraseña a {user.email}: {str(e)}')
            return False
