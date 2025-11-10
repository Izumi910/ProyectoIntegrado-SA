from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse

def requiere_permiso(permiso, modulo=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('usuarios:login')
            
            # Debug: Verificar usuario
            if request.user.username == 'admin':
                # Admin siempre pasa
                return view_func(request, *args, **kwargs)
            
            # Para otros usuarios, verificar permisos
            if modulo and permiso:
                campo_permiso = f'puede_{permiso}_{modulo}'
                if not getattr(request.user, campo_permiso, False):
                    messages.error(request, f'No tienes permisos para {permiso} en {modulo}.')
                    return redirect('usuarios:dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator