import logging
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils import timezone

logger = logging.getLogger('security')

class SingleSessionMiddleware:
    """
    Middleware que previene múltiples sesiones simultáneas del mismo usuario.
    Solo permite una sesión activa por usuario.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtener la sesión actual del usuario
            current_session_key = request.session.session_key
            
            # Buscar si el usuario tiene una sesión guardada
            stored_session_key = request.user.last_session_key if hasattr(request.user, 'last_session_key') else None
            
            # Si hay una sesión guardada y es diferente a la actual
            if stored_session_key and stored_session_key != current_session_key:
                try:
                    # Verificar si la sesión anterior aún existe
                    old_session = Session.objects.filter(session_key=stored_session_key).first()
                    
                    if old_session and old_session.expire_date > timezone.now():
                        # Hay otra sesión activa - cerrar esta sesión
                        logger.warning(
                            f'Intento de sesión múltiple detectado para usuario {request.user.username} '
                            f'desde IP {request.META.get("REMOTE_ADDR")}'
                        )
                        
                        logout(request)
                        messages.error(
                            request, 
                            'Tu cuenta ya tiene una sesión activa en otro dispositivo. '
                            'Por seguridad, solo se permite una sesión a la vez.'
                        )
                        return redirect('usuarios:login')
                    else:
                        # La sesión anterior expiró, actualizar con la nueva
                        request.user.last_session_key = current_session_key
                        request.user.save(update_fields=['last_session_key'])
                        
                except Exception as e:
                    logger.error(f'Error verificando sesión para {request.user.username}: {str(e)}')
            
            elif not stored_session_key:
                # Primera sesión del usuario, guardarla
                request.user.last_session_key = current_session_key
                request.user.save(update_fields=['last_session_key'])

        response = self.get_response(request)
        return response


class SecurityMiddleware:
    """
    Middleware de seguridad adicional para validaciones y logging
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Validar usuario activo
        if request.user.is_authenticated:
            if hasattr(request.user, 'estado') and request.user.estado != 'ACTIVO':
                logger.warning(
                    f'Usuario inactivo {request.user.username} intentó acceder '
                    f'desde IP {request.META.get("REMOTE_ADDR")}'
                )
                logout(request)
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                return redirect('usuarios:login')
        
        response = self.get_response(request)
        return response
