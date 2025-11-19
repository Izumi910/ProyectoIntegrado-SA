import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from .models import Usuario
from .services import EmailService

logger = logging.getLogger('django')

# Variable global para trackear contraseñas
_password_tracker = {}

@receiver(pre_save, sender=Usuario)
def track_password_before_save(sender, instance, **kwargs):
    """Guarda la contraseña original antes de guardar"""
    if instance.pk:
        try:
            original = Usuario.objects.get(pk=instance.pk)
            _password_tracker[instance.pk] = original.password
        except Usuario.DoesNotExist:
            pass

@receiver(post_save, sender=Usuario)
def handle_user_post_save(sender, instance, created, **kwargs):
    """Maneja creación de usuario y cambio de contraseña"""
    
    # CASO 1: Usuario nuevo creado
    if created and instance.email:
        try:
            # Generar contraseña segura
            password = EmailService.generate_secure_password()
            
            # Asignar contraseña
            instance.set_password(password)
            
            # Guardar sin disparar signal nuevamente
            Usuario.objects.filter(pk=instance.pk).update(password=instance.password)
            
            # Enviar email
            EmailService.send_new_user_email(instance, password)
            
            logger.info(f'Usuario {instance.username} creado con contraseña automática')
            
        except Exception as e:
            logger.error(f'Error procesando nuevo usuario {instance.username}: {str(e)}')
    
    # CASO 2: Cambio de contraseña en usuario existente
    elif not created and instance.pk in _password_tracker:
        original_password = _password_tracker.pop(instance.pk)
        
        # Verificar si cambió la contraseña
        if original_password != instance.password and instance.email:
            try:
                EmailService.send_password_changed_email(instance)
                logger.info(f'Contraseña cambiada para {instance.username}')
            except Exception as e:
                logger.error(f'Error enviando email de cambio de contraseña: {str(e)}')

@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    """Maneja el login del usuario y guarda la sesión"""
    try:
        # Guardar IP del login
        user.last_login_ip = request.META.get('REMOTE_ADDR')
        
        # Guardar la clave de sesión actual
        user.last_session_key = request.session.session_key
        
        # Resetear intentos fallidos
        user.failed_login_attempts = 0
        user.account_locked_until = None
        
        user.save(update_fields=['last_login_ip', 'last_session_key', 'failed_login_attempts', 'account_locked_until'])
        
        logger.info(f'Usuario {user.username} inició sesión desde IP {user.last_login_ip}')
        
    except Exception as e:
        logger.error(f'Error en handle_user_login para {user.username}: {str(e)}')

@receiver(user_logged_out)
def handle_user_logout(sender, request, user, **kwargs):
    """Limpia la sesión al hacer logout"""
    if user:
        try:
            # Limpiar la sesión guardada
            user.last_session_key = None
            user.save(update_fields=['last_session_key'])
            
            logger.info(f'Usuario {user.username} cerró sesión')
            
        except Exception as e:
            logger.error(f'Error en handle_user_logout para {user.username}: {str(e)}')
