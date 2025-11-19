import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from proveedores.models import Proveedor

class Command(BaseCommand):
    help = 'Genera proveedores de prueba para stress testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=10000,
            help='Cantidad de proveedores a generar (default: 10000)'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        self.stdout.write(self.style.WARNING(f'Generando {cantidad} proveedores de prueba...'))
        
        # Generar proveedores en lotes
        batch_size = 1000
        total_creados = 0
        
        for i in range(0, cantidad, batch_size):
            lote_size = min(batch_size, cantidad - i)
            proveedores = self._generar_lote_proveedores(i, lote_size)
            
            with transaction.atomic():
                Proveedor.objects.bulk_create(proveedores, ignore_conflicts=True)
            
            total_creados += lote_size
            self.stdout.write(
                self.style.SUCCESS(f'Creados {total_creados}/{cantidad} proveedores...')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Se generaron {cantidad} proveedores exitosamente!')
        )

    def _generar_lote_proveedores(self, inicio, cantidad):
        """Genera un lote de proveedores"""
        proveedores = []
        
        # Obtener el ultimo RUT
        ultimo_proveedor = Proveedor.objects.filter(rut_nif__startswith='RUT-').order_by('-rut_nif').first()
        if ultimo_proveedor:
            ultimo_num = int(ultimo_proveedor.rut_nif.split('-')[1])
        else:
            ultimo_num = 0
        
        tipos_empresa = ['Distribuidora', 'Importadora', 'Fabricante', 'Mayorista', 'Comercial']
        rubros = ['Alimentos', 'Dulces', 'Bebidas', 'Snacks', 'Confiteria', 'Chocolates']
        ciudades = ['Santiago', 'Valparaiso', 'Concepcion', 'La Serena', 'Antofagasta', 'Temuco', 'Vina del Mar']
        condiciones = ['Contado', '30 dias', '60 dias', '90 dias', '15 dias', '45 dias']
        monedas = ['CLP', 'USD', 'EUR']
        
        nombres = ['Global', 'Premium', 'Express', 'Direct', 'Quality', 'Best', 'Top', 'Elite', 'Prime', 'Master']
        apellidos = ['Trading', 'Supply', 'Group', 'Corp', 'International', 'Solutions', 'Services', 'Partners']
        
        for i in range(cantidad):
            num = ultimo_num + inicio + i + 1
            
            tipo = random.choice(tipos_empresa)
            rubro = random.choice(rubros)
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            
            razon_social = f'{tipo} {nombre} {apellido} {rubro} S.A.'
            nombre_fantasia = f'{nombre} {rubro}'
            
            proveedor = Proveedor(
                rut_nif=f'RUT-{num:08d}',
                razon_social=razon_social,
                nombre_fantasia=nombre_fantasia,
                email=f'contacto{num}@{nombre.lower()}{apellido.lower()}.cl',
                telefono=f'+569{random.randint(10000000, 99999999)}',
                sitio_web=f'https://www.{nombre.lower()}{apellido.lower()}.cl',
                direccion=f'Av. Principal {random.randint(100, 9999)}, Of. {random.randint(1, 50)}',
                ciudad=random.choice(ciudades),
                pais='Chile',
                condiciones_pago=random.choice(condiciones),
                moneda=random.choice(monedas),
                contacto_principal_nombre=f'{random.choice(["Juan", "Maria", "Pedro", "Ana", "Carlos", "Sofia"])} {random.choice(["Perez", "Gonzalez", "Rodriguez", "Martinez", "Lopez"])}',
                contacto_principal_email=f'ventas{num}@{nombre.lower()}{apellido.lower()}.cl',
                contacto_principal_telefono=f'+569{random.randint(10000000, 99999999)}',
                estado=random.choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'INACTIVO']),  # 75% activos
                observaciones=f'Proveedor de prueba #{num} - {rubro}'
            )
            
            proveedores.append(proveedor)
        
        return proveedores
