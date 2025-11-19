#!/usr/bin/env python
"""
Script para poblar la base de datos AWS con datos de prueba
Ejecutar en la instancia AWS después del despliegue
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from django.core.management import call_command
from productos.models import Producto
from proveedores.models import Proveedor

def main():
    print("=" * 60)
    print("POBLANDO BASE DE DATOS AWS CON DATOS DE PRUEBA")
    print("=" * 60)
    
    # Verificar estado actual
    productos_count = Producto.objects.count()
    proveedores_count = Proveedor.objects.count()
    
    print(f"\nEstado actual:")
    print(f"  Productos: {productos_count}")
    print(f"  Proveedores: {proveedores_count}")
    
    # Generar productos si no existen
    if productos_count < 10000:
        print(f"\nGenerando {10000 - productos_count} productos...")
        call_command('generate_test_products', cantidad=10000 - productos_count)
    else:
        print("\nProductos ya generados. Saltando...")
    
    # Generar proveedores si no existen
    if proveedores_count < 10000:
        print(f"\nGenerando {10000 - proveedores_count} proveedores...")
        call_command('generate_test_proveedores', cantidad=10000 - proveedores_count)
    else:
        print("\nProveedores ya generados. Saltando...")
    
    # Verificar resultado final
    productos_final = Producto.objects.count()
    proveedores_final = Proveedor.objects.count()
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL:")
    print("=" * 60)
    print(f"  Productos: {productos_final}")
    print(f"  Proveedores: {proveedores_final}")
    print("\n¡Datos generados exitosamente!")
    print("=" * 60)

if __name__ == '__main__':
    main()
