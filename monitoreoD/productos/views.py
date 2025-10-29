from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
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
    # Búsqueda
    search = request.GET.get('search', '')
    # Ordenamiento
    order_by = request.GET.get('order_by', 'nombre')
    # Paginación
    per_page = request.GET.get('per_page', '10')
    
    productos = Producto.objects.all()
    
    # Aplicar búsqueda
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) | 
            Q(sku__icontains=search) | 
            Q(categoria__nombre__icontains=search)
        )
    
    # Aplicar ordenamiento
    if order_by in ['nombre', '-nombre', 'sku', '-sku', 'precio_venta', '-precio_venta', 'stock', '-stock']:
        productos = productos.order_by(order_by)
    
    # Paginación
    paginator = Paginator(productos, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'order_by': order_by,
        'per_page': per_page,
    }
    
    return render(request, "productos/lista.html", context)

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect("productos:productos_lista")
    else:
        form = ProductoForm()
    return render(request, "productos/crear.html", {"form": form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect("productos:productos_lista")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/editar.html", {"form": form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect("productos:productos_lista")
    return render(request, "productos/eliminar.html", {"producto": producto})

@login_required
def panel_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/panel.html', {'productos': productos})

@login_required
def inicio(request):
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1

    return render(request, 'productos/inicio.html', {'visitas': visitas})







