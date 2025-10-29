from django.shortcuts import render
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu email'})
    )

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(email=email)
                # Enviar email con instrucciones
                subject = 'Recuperación de Contraseña - Lilis Dulcería'
                message = f'''Hola {usuario.username},

Has solicitado recuperar tu contraseña para el sistema de Lilis Dulcería.

Sigue estas instrucciones:

1. Contacta al administrador del sistema para solicitar el cambio de contraseña
2. Proporciona tu nombre de usuario: {usuario.username}

Si no solicitaste este cambio, ignora este mensaje.

Saludos,
Equipo de Lilis Dulcería'''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Se han enviado las instrucciones a tu email.')
                return redirect('usuarios:login')
            except Usuario.DoesNotExist:
                messages.error(request, 'No existe un usuario con ese email.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'usuarios/password_reset.html', {'form': form})

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente.')
            return redirect('usuarios:usuarios_lista')
    else:
        form = UsuarioChangeForm(instance=usuario)
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario, 'title': 'Editar Usuario'})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado exitosamente.')
            return redirect('usuarios:usuarios_lista')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/crear.html', {'form': form, 'title': 'Crear Usuario'})

@login_required
def lista_usuarios(request):
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'username')
    per_page = request.GET.get('per_page', '10')
    
    usuarios = Usuario.objects.all()
    
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) | 
            Q(email__icontains=search) | 
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search)
        )
    
    if order_by in ['username', '-username', 'email', '-email', 'date_joined', '-date_joined']:
        usuarios = usuarios.order_by(order_by)
    
    paginator = Paginator(usuarios, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'order_by': order_by,
        'per_page': per_page,
    }
    
    return render(request, 'usuarios/lista.html', context)

@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username}" eliminado exitosamente.')
        return redirect('usuarios:usuarios_lista')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

@login_required
def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalle.html', {'usuario': usuario})

