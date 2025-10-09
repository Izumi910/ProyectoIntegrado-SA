from django.shortcuts import render
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioChangeForm(instance=usuario)
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario, 'title': 'Editar Usuario'})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/crear.html', {'form': form, 'title': 'Crear Usuario'})

@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios:lista')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

@login_required
def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalle.html', {'usuario': usuario})

