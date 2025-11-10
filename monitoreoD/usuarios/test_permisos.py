from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import requiere_permiso

@login_required
@requiere_permiso('ver', 'productos')
def test_productos(request):
    return HttpResponse(f"Usuario: {request.user.username}, Rol: {request.user.rol}, Puede ver productos: {request.user.puede_ver_productos}")

@login_required  
def test_sin_decorador(request):
    return HttpResponse(f"Usuario: {request.user.username}, Rol: {request.user.rol}, Sin decorador funciona")