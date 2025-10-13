from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

@login_required
def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        contraseña = request.POST.get("contraseña")
        user = authenticate(request, username=usuario, password=contraseña)
        if user is not None:
            login(request, user)
            return redirect("productos:lista")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "productos/login.html")

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/inicio.html", {"productos": productos})

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:lista")
    else:
        form = ProductoForm()
    return render(request, "productos/crear.html", {"form": form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("productos:lista")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/editar.html", {"form": form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("productos:lista")
    return render(request, "productos/eliminar.html", {"producto": producto})

@login_required
def panel_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/panel.html', {'productos': productos})









