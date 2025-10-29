from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import MovimientoInventario
from .forms import MovimientoInventarioForm

def lista_movimientos(request):
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '-fecha')
    per_page = request.GET.get('per_page', '10')
    
    movimientos = MovimientoInventario.objects.all()
    
    if search:
        movimientos = movimientos.filter(
            Q(producto__nombre__icontains=search) | 
            Q(tipo__icontains=search) | 
            Q(lote__icontains=search)
        )
    
    if order_by in ['fecha', '-fecha', 'tipo', '-tipo', 'cantidad', '-cantidad', 'producto__nombre', '-producto__nombre']:
        movimientos = movimientos.order_by(order_by)
    
    paginator = Paginator(movimientos, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'order_by': order_by,
        'per_page': per_page,
    }
    
    return render(request, 'inventario/lista.html', context)

def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save()
            messages.success(request, f'Movimiento de inventario creado exitosamente.')
            return redirect('inventario:inventario_lista')
    else:
        form = MovimientoInventarioForm()
    return render(request, 'inventario/crear.html', {'form': form})

def editar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Movimiento de inventario actualizado exitosamente.')
            return redirect('inventario:inventario_lista')
    else:
        form = MovimientoInventarioForm(instance=movimiento)
    return render(request, 'inventario/editar.html', {'form': form, 'movimiento': movimiento})

def eliminar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, f'Movimiento de inventario eliminado exitosamente.')
        return redirect('inventario:inventario_lista')
    return render(request, 'inventario/eliminar.html', {'movimiento': movimiento})

def detalle_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    return render(request, 'inventario/detalle.html', {'movimiento': movimiento})