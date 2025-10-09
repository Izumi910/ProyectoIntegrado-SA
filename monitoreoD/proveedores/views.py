from django.shortcuts import render, get_object_or_404, redirect
from .models import Proveedor, ProveedorProducto
from .forms import ProveedorForm, ProveedorProductoForm

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/crear.html', {'form': form})

def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar.html', {'form': form, 'proveedor': proveedor})

def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores:lista')
    return render(request, 'proveedores/eliminar.html', {'proveedor': proveedor})

def detalle_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedores/detalle.html', {'proveedor': proveedor})



def lista_proveedor_productos(request):
    relaciones = ProveedorProducto.objects.all()
    return render(request, 'proveedores/lista_proveedor_productos.html', {'relaciones': relaciones})

def crear_proveedor_producto(request):
    if request.method == 'POST':
        form = ProveedorProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista_proveedor_productos')
    else:
        form = ProveedorProductoForm()
    return render(request, 'proveedores/crear_proveedor_producto.html', {'form': form})

def editar_proveedor_producto(request, pk):
    relacion = get_object_or_404(ProveedorProducto, pk=pk)
    if request.method == 'POST':
        form = ProveedorProductoForm(request.POST, instance=relacion)
        if form.is_valid():
            form.save()
            return redirect('proveedores:lista_proveedor_productos')