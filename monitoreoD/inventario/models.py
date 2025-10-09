from django.db import models
from productos.models import Producto
from proveedores.models import Proveedor

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6)
    lote = models.CharField(max_length=50, blank=True, null=True)
    serie = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto} - {self.fecha}"