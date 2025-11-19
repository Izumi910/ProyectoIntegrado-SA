import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from productos.models import Producto, Categoria
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Genera 5000 productos de prueba para stress testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=5000,
            help='Cantidad de productos a generar (default: 5000)'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        self.stdout.write(self.style.WARNING(f'Generando {cantidad} productos de prueba...'))
        
        # Crear categorías si no existen
        categorias = self._crear_categorias()
        
        # Generar productos en lotes para mejor performance
        batch_size = 500
        total_creados = 0
        
        for i in range(0, cantidad, batch_size):
            lote_size = min(batch_size, cantidad - i)
            productos = self._generar_lote_productos(i, lote_size, categorias)
            
            # Inserción masiva
            with transaction.atomic():
                Producto.objects.bulk_create(productos, ignore_conflicts=True)
            
            total_creados += lote_size
            self.stdout.write(
                self.style.SUCCESS(f'Creados {total_creados}/{cantidad} productos...')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Se generaron {cantidad} productos exitosamente!')
        )

    def _crear_categorias(self):
        """Crea categorías de prueba"""
        categorias_nombres = [
            'Dulces', 'Chocolates', 'Caramelos', 'Gomitas', 'Chicles',
            'Galletas', 'Snacks', 'Bebidas', 'Helados', 'Postres',
            'Frutas Confitadas', 'Turrones', 'Mazapanes', 'Bombones', 'Paletas'
        ]
        
        categorias = []
        for nombre in categorias_nombres:
            cat, created = Categoria.objects.get_or_create(nombre=nombre)
            categorias.append(cat)
        
        return categorias

    def _generar_lote_productos(self, inicio, cantidad, categorias):
        """Genera un lote de productos"""
        productos = []
        
        # Obtener el último SKU existente
        ultimo_producto = Producto.objects.filter(sku__startswith='SKU-').order_by('-sku').first()
        if ultimo_producto:
            ultimo_num = int(ultimo_producto.sku.split('-')[1])
        else:
            ultimo_num = 0
        
        marcas = ['Nestlé', 'Ferrero', 'Mars', 'Hershey', 'Cadbury', 'Lindt', 'Toblerone', 'Milka']
        tipos = ['Premium', 'Clásico', 'Light', 'Sin Azúcar', 'Orgánico', 'Artesanal']
        sabores = ['Chocolate', 'Fresa', 'Vainilla', 'Limón', 'Naranja', 'Menta', 'Caramelo', 'Coco']
        
        for i in range(cantidad):
            num = ultimo_num + inicio + i + 1
            
            # Generar datos aleatorios
            marca = random.choice(marcas)
            tipo = random.choice(tipos)
            sabor = random.choice(sabores)
            categoria = random.choice(categorias)
            
            # Generar precios realistas
            costo = Decimal(random.uniform(100, 5000)).quantize(Decimal('0.01'))
            margen = Decimal(random.uniform(1.2, 2.5))
            precio = (costo * margen).quantize(Decimal('0.01'))
            
            producto = Producto(
                sku=f'SKU-{num:06d}',
                ean_upc=f'{random.randint(1000000000000, 9999999999999)}',
                nombre=f'{marca} {tipo} {sabor} #{num}',
                descripcion=f'Producto de prueba {num} - {tipo} sabor {sabor}',
                categoria=categoria,
                marca=marca,
                modelo=f'MOD-{num}',
                uom_compra='unidad',
                uom_venta='unidad',
                factor_conversion=Decimal('1.00'),
                costo_estandar=costo,
                costo_promedio=costo,
                precio_venta=precio,
                impuesto_iva=Decimal('19.00'),
                stock_minimo=random.randint(10, 50),
                stock_maximo=random.randint(100, 500),
                punto_reorden=random.randint(20, 80),
                perishable=random.choice([True, False]),
                control_por_lote=random.choice([True, False]),
                control_por_serie=False,
                stock=random.randint(0, 300),
                lote=f'LOTE-{random.randint(1000, 9999)}' if random.choice([True, False]) else None,
                fecha_vencimiento=datetime.now().date() + timedelta(days=random.randint(30, 365)) if random.choice([True, False]) else None,
                estado=random.choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'INACTIVO'])  # 75% activos
            )
            
            productos.append(producto)
        
        return productos
