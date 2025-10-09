from django.shortcuts import render, get_object_or_404, redirect
from .models import MovimientoInventario
from .forms import MovimientoInventarioForm

def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.all()
    return render(request, 'inventario/lista.html', {'movimientos': movimientos})

def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista')
    else:
        form = MovimientoInventarioForm()
    return render(request, 'inventario/crear.html', {'form': form})

def editar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista')
    else:
        form = MovimientoInventarioForm(instance=movimiento)
    return render(request, 'inventario/editar.html', {'form': form, 'movimiento': movimiento})

def eliminar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        return redirect('inventario:lista')
    return render(request, 'inventario/eliminar.html', {'movimiento': movimiento})

def detalle_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    return render(request, 'inventario/detalle.html', {'movimiento': movimiento})