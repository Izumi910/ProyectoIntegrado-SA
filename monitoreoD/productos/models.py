from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True, default='SKU_TEMP')

    ean_upc = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)

    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    uom_compra = models.CharField(max_length=10, default="unidad")
    uom_venta = models.CharField(max_length=10, default="unidad")
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    costo_estandar = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    costo_promedio = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    impuesto_iva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)

    stock_minimo = models.IntegerField(default=0)
    stock_maximo = models.IntegerField(blank=True, null=True)
    punto_reorden = models.IntegerField(blank=True, null=True)
    perishable = models.BooleanField(default=False)
    control_por_lote = models.BooleanField(default=False)
    control_por_serie = models.BooleanField(default=False)
    imagen_url = models.URLField(blank=True, null=True)
    ficha_tecnica_url = models.URLField(blank=True, null=True)

    # 👇 Campos nuevos
    stock = models.IntegerField(default=0)
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    
    @property
    def stock_actual(self):
        from inventario.models import MovimientoInventario
        ingresos = MovimientoInventario.objects.filter(producto=self, tipo='INGRESO').aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0
        salidas = MovimientoInventario.objects.filter(producto=self, tipo='SALIDA').aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0
        return ingresos - salidas

    @property
    def alerta_bajo_stock(self):
        return self.stock_actual <= self.stock_minimo
    
    def __str__(self):
        return self.nombre




