from django.shortcuts import render, get_object_or_404, redirect
from .models import Proveedor, ProveedorProducto
from .forms import ProveedorForm, ProveedorProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def lista_proveedores(request):
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'razon_social')
    per_page = request.GET.get('per_page', '10')
    
    proveedores = Proveedor.objects.all()
    
    if search:
        proveedores = proveedores.filter(
            Q(razon_social__icontains=search) | 
            Q(rut_nif__icontains=search) | 
            Q(email__icontains=search) | 
            Q(ciudad__icontains=search)
        )
    
    if order_by in ['razon_social', '-razon_social', 'rut_nif', '-rut_nif', 'email', '-email', 'ciudad', '-ciudad']:
        proveedores = proveedores.order_by(order_by)
    
    paginator = Paginator(proveedores, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'order_by': order_by,
        'per_page': per_page,
    }
    
    return render(request, 'proveedores/lista.html', context)

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.razon_social}" creado exitosamente.')
            return redirect('proveedores:proveedores_lista')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/crear.html', {'form': form})

@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.razon_social}" actualizado exitosamente.')
            return redirect('proveedores:proveedores_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar.html', {'form': form, 'proveedor': proveedor})

@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        razon_social = proveedor.razon_social
        proveedor.delete()
        messages.success(request, f'Proveedor "{razon_social}" eliminado exitosamente.')
        return redirect('proveedores:proveedores_lista')
    return render(request, 'proveedores/eliminar.html', {'proveedor': proveedor})

@login_required
def detalle_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedores/detalle.html', {'proveedor': proveedor})


@login_required
def lista_proveedor_productos(request):
    relaciones = ProveedorProducto.objects.all()
    return render(request, 'proveedores/lista_proveedor_productos.html', {'relaciones': relaciones})

@login_required
def crear_proveedor_producto(request):
    if request.method == 'POST':
        form = ProveedorProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista_proveedor_productos')
    else:
        form = ProveedorProductoForm()
    return render(request, 'proveedores/crear_proveedor_producto.html', {'form': form})

@login_required
def editar_proveedor_producto(request, pk):
    relacion = get_object_or_404(ProveedorProducto, pk=pk)
    if request.method == 'POST':
        form = ProveedorProductoForm(request.POST, instance=relacion)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista_proveedor_productos')