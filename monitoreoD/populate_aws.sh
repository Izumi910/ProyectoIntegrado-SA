#!/bin/bash
# Script para poblar base de datos AWS con datos de prueba
# Ejecutar en la instancia AWS

echo "=========================================="
echo "POBLANDO BASE DE DATOS AWS"
echo "=========================================="

# Detectar si estamos en Elastic Beanstalk o EC2
if [ -d "/var/app/current" ]; then
    echo "Detectado: Elastic Beanstalk"
    cd /var/app/current
    source /var/app/venv/*/bin/activate
elif [ -d "/var/www/lilis" ]; then
    echo "Detectado: EC2"
    cd /var/www/lilis
    source venv/bin/activate
else
    echo "Error: No se detectó la ubicación del proyecto"
    exit 1
fi

echo ""
echo "Directorio actual: $(pwd)"
echo "Python: $(which python)"
echo ""

# Ejecutar script de población
python populate_aws_data.py

# Verificar resultado
echo ""
echo "Verificando datos..."
python manage.py shell -c "
from productos.models import Producto
from proveedores.models import Proveedor
print(f'✓ Productos: {Producto.objects.count()}')
print(f'✓ Proveedores: {Proveedor.objects.count()}')
"

echo ""
echo "=========================================="
echo "¡COMPLETADO!"
echo "=========================================="
