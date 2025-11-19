# 📦 MIGRAR DATOS A AWS RDS

## OPCIÓN 1: Ejecutar Comandos en AWS (Recomendado)

### Paso 1: Conectar a tu instancia AWS

```bash
# Si usas Elastic Beanstalk
eb ssh

# Si usas EC2
ssh -i tu-key.pem ubuntu@tu-ec2-ip
```

### Paso 2: Activar entorno virtual y generar datos

```bash
# Navegar al directorio del proyecto
cd /var/app/current  # Para EB
# o
cd /var/www/lilis    # Para EC2

# Activar entorno virtual
source /var/app/venv/*/bin/activate  # Para EB
# o
source venv/bin/activate  # Para EC2

# Generar productos
python manage.py generate_test_products --cantidad 10000

# Generar proveedores
python manage.py generate_test_proveedores --cantidad 10000
```

---

## OPCIÓN 2: Exportar e Importar con mysqldump

### Paso 1: Exportar datos locales

```bash
# En tu máquina local
cd monitoreoD

# Exportar solo datos (sin estructura)
python manage.py dumpdata productos.Producto productos.Categoria > productos_data.json
python manage.py dumpdata proveedores.Proveedor > proveedores_data.json
```

### Paso 2: Subir archivos a AWS

```bash
# Copiar a instancia EC2
scp -i tu-key.pem productos_data.json ubuntu@tu-ec2-ip:/tmp/
scp -i tu-key.pem proveedores_data.json ubuntu@tu-ec2-ip:/tmp/

# O para Elastic Beanstalk
eb ssh
# Luego desde tu local en otra terminal:
scp -i ~/.ssh/tu-key.pem productos_data.json ec2-user@tu-eb-ip:/tmp/
```

### Paso 3: Importar en AWS

```bash
# Conectar a AWS
eb ssh  # o ssh a EC2

# Navegar al proyecto
cd /var/app/current

# Activar entorno
source /var/app/venv/*/bin/activate

# Importar datos
python manage.py loaddata /tmp/productos_data.json
python manage.py loaddata /tmp/proveedores_data.json
```

---

## OPCIÓN 3: Dump SQL Directo (Más Rápido)

### Paso 1: Exportar base de datos local

```bash
# Si usas MySQL local
mysqldump -u root -p BD_Lilis productos_producto productos_categoria > productos.sql
mysqldump -u root -p BD_Lilis proveedores_proveedor > proveedores.sql
```

### Paso 2: Importar a RDS

```bash
# Conectar a RDS desde tu máquina local
mysql -h tu-rds-endpoint.rds.amazonaws.com -u admin -p lilis_production < productos.sql
mysql -h tu-rds-endpoint.rds.amazonaws.com -u admin -p lilis_production < proveedores.sql
```

---

## OPCIÓN 4: Script de Migración Automático

Crear archivo `migrate_data_to_rds.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from django.core.management import call_command

print("Generando productos...")
call_command('generate_test_products', cantidad=10000)

print("Generando proveedores...")
call_command('generate_test_proveedores', cantidad=10000)

print("Datos generados exitosamente!")
```

Ejecutar en AWS:

```bash
python migrate_data_to_rds.py
```

---

## OPCIÓN 5: Usar Django Admin para Importar

### Paso 1: Exportar a CSV/Excel

```bash
# En local
python manage.py shell
```

```python
import csv
from productos.models import Producto

with open('productos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['sku', 'nombre', 'precio_venta', 'stock', ...])
    
    for p in Producto.objects.all():
        writer.writerow([p.sku, p.nombre, p.precio_venta, p.stock, ...])
```

### Paso 2: Crear comando de importación

Crear `usuarios/management/commands/import_csv.py`:

```python
import csv
from django.core.management.base import BaseCommand
from productos.models import Producto, Categoria

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        with open(options['file'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Producto.objects.create(**row)
```

---

## 🚀 MÉTODO RECOMENDADO (MÁS SIMPLE)

### Ejecutar directamente en AWS:

```bash
# 1. Conectar a AWS
eb ssh

# 2. Ir al directorio del proyecto
cd /var/app/current

# 3. Activar entorno
source /var/app/venv/*/bin/activate

# 4. Generar datos
python manage.py generate_test_products --cantidad 10000
python manage.py generate_test_proveedores --cantidad 10000

# 5. Verificar
python manage.py shell -c "from productos.models import Producto; print(f'Productos: {Producto.objects.count()}')"
```

**Tiempo estimado: 5-10 minutos**

---

## ⚡ MÉTODO MÁS RÁPIDO (Si tienes acceso directo a RDS)

### Conectar directamente a RDS y ejecutar comandos:

```bash
# 1. Configurar túnel SSH (si es necesario)
ssh -i tu-key.pem -L 3307:tu-rds-endpoint:3306 ubuntu@tu-ec2-ip

# 2. En otra terminal, conectar a través del túnel
mysql -h 127.0.0.1 -P 3307 -u admin -p

# 3. Importar dump SQL
mysql -h 127.0.0.1 -P 3307 -u admin -p lilis_production < backup.sql
```

---

## 🔍 VERIFICAR DATOS EN AWS

```bash
# Conectar a AWS
eb ssh

# Verificar productos
python manage.py shell -c "from productos.models import Producto; print(Producto.objects.count())"

# Verificar proveedores
python manage.py shell -c "from proveedores.models import Proveedor; print(Proveedor.objects.count())"

# Ver primeros registros
python manage.py shell -c "from productos.models import Producto; print(list(Producto.objects.all()[:5].values('sku', 'nombre')))"
```

---

## ❌ SOLUCIÓN DE PROBLEMAS

### Error: "Command not found"
**Solución:** Asegúrate de estar en el directorio correcto y con el entorno virtual activado

### Error: "Permission denied"
**Solución:** Usa `sudo` o verifica permisos del usuario

### Error: "Database connection failed"
**Solución:** Verifica las variables de entorno y Security Groups de RDS

### Los comandos tardan mucho
**Solución:** Normal, 10,000 registros pueden tardar 5-10 minutos

---

## 📝 CHECKLIST

- [ ] Conectado a instancia AWS
- [ ] Entorno virtual activado
- [ ] Variables de entorno configuradas
- [ ] Migraciones aplicadas
- [ ] Comandos de generación ejecutados
- [ ] Datos verificados
- [ ] Aplicación reiniciada (si es necesario)

---

## 🎯 COMANDO TODO-EN-UNO

Crear script `populate_aws.sh`:

```bash
#!/bin/bash
echo "Activando entorno..."
source /var/app/venv/*/bin/activate

echo "Generando productos..."
python manage.py generate_test_products --cantidad 10000

echo "Generando proveedores..."
python manage.py generate_test_proveedores --cantidad 10000

echo "Verificando datos..."
python manage.py shell -c "from productos.models import Producto; from proveedores.models import Proveedor; print(f'Productos: {Producto.objects.count()}'); print(f'Proveedores: {Proveedor.objects.count()}')"

echo "¡Completado!"
```

Ejecutar:

```bash
chmod +x populate_aws.sh
./populate_aws.sh
```
