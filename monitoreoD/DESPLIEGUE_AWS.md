# 🚀 GUÍA DE DESPLIEGUE A AWS

## ✅ CHECKLIST PRE-DESPLIEGUE

### Código y Configuración
- [x] Sistema de autenticación funcionando
- [x] Sistema de permisos implementado
- [x] Sesión única por usuario
- [x] Bloqueo de usuarios inactivos
- [x] Control de intentos fallidos
- [x] Envío de emails configurado
- [x] Generación de contraseñas seguras
- [x] Middleware de seguridad
- [x] Logging implementado
- [x] Configuración de archivos estáticos
- [x] Configuración de archivos media
- [ ] Configuración de producción separada
- [ ] Variables de entorno documentadas
- [ ] Requirements.txt actualizado
- [ ] Migraciones aplicadas

### Base de Datos
- [x] 10,007 productos de prueba
- [x] 10,002 proveedores de prueba
- [x] Usuarios de prueba creados
- [x] Migraciones funcionando
- [ ] Backup de base de datos
- [ ] Script de migración a RDS

---

## 📋 PREPARACIÓN DEL PROYECTO

### 1. Crear requirements.txt completo

```bash
pip freeze > requirements.txt
```

O crear manualmente:

```txt
Django>=5.2.0
python-dotenv>=1.0.0
mysqlclient>=2.2.0
django-ses>=3.5.0
boto3>=1.28.0
gunicorn>=21.2.0
whitenoise>=6.5.0
psycopg2-binary>=2.9.0
redis>=4.5.0
openpyxl>=3.1.0
Pillow>=10.0.0
```

### 2. Crear archivo .gitignore

```
*.pyc
__pycache__/
*.sqlite3
db.sqlite3
.env
*.log
media/
staticfiles/
.DS_Store
venv/
env/
*.swp
*.swo
.vscode/
.idea/
```

### 3. Configurar archivos estáticos

Actualizar `settings.py`:

```python
# Archivos estáticos para producción
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Usar WhiteNoise para servir archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregar después de SecurityMiddleware
    # ... resto de middlewares
]

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. Crear archivo runtime.txt (para Elastic Beanstalk)

```
python-3.12
```

---

## 🎯 OPCIÓN 1: AWS ELASTIC BEANSTALK (Recomendado)

### Ventajas:
- Despliegue más simple
- Auto-scaling automático
- Load balancer incluido
- Monitoreo integrado
- Ideal para Django

### Paso 1: Instalar EB CLI

```bash
pip install awsebcli
```

### Paso 2: Inicializar Elastic Beanstalk

```bash
cd monitoreoD
eb init -p python-3.12 lilis-dulceria --region us-east-1
```

### Paso 3: Crear archivo .ebextensions/django.config

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: monitoreo.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: monitoreo.settings
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: staticfiles

container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
  03_createsu:
    command: "source /var/app/venv/*/bin/activate && python manage.py shell < create_superuser.py"
    leader_only: true
    ignoreErrors: true
```

### Paso 4: Crear script create_superuser.py

```python
from usuarios.models import Usuario
from django.db import IntegrityError

try:
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create_superuser(
            username='admin',
            email='admin@lilis.com',
            password='ChangeMe123!',
            rol='ADMINISTRADOR'
        )
        print("Superuser created")
except IntegrityError:
    print("Superuser already exists")
```

### Paso 5: Configurar variables de entorno en EB

```bash
eb setenv \
  DJANGO_SECRET_KEY="tu-secret-key-super-segura-aqui" \
  DJANGO_DEBUG=False \
  DJANGO_ENV=production \
  ALLOWED_HOSTS=".elasticbeanstalk.com,tudominio.com" \
  DB_ENGINE=mysql \
  DB_NAME=lilis_db \
  DB_USER=admin \
  DB_PASSWORD=tu_password_seguro \
  DB_HOST=tu-rds-endpoint.rds.amazonaws.com \
  DB_PORT=3306 \
  AWS_ACCESS_KEY_ID=tu_access_key \
  AWS_SECRET_ACCESS_KEY=tu_secret_key \
  AWS_SES_REGION=us-east-1 \
  DEFAULT_FROM_EMAIL=noreply@tudominio.com \
  REDIS_URL=redis://tu-elasticache-endpoint:6379/0
```

### Paso 6: Crear entorno y desplegar

```bash
# Crear entorno
eb create lilis-prod --database.engine mysql --database.username admin

# Desplegar
eb deploy

# Ver logs
eb logs

# Abrir en navegador
eb open
```

---

## 🎯 OPCIÓN 2: AWS EC2 + RDS + S3

### Paso 1: Crear instancia EC2

1. Ir a EC2 Console
2. Launch Instance
3. Seleccionar Ubuntu Server 22.04 LTS
4. Tipo: t3.medium (mínimo)
5. Configurar Security Group:
   - SSH (22) - Tu IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - MySQL (3306) - Security Group de RDS

### Paso 2: Crear base de datos RDS

1. Ir a RDS Console
2. Create Database
3. MySQL 8.0
4. Free tier o db.t3.micro
5. Nombre: lilis-db
6. Usuario: admin
7. Guardar endpoint

### Paso 3: Conectar a EC2 y configurar

```bash
# Conectar a EC2
ssh -i tu-key.pem ubuntu@tu-ec2-ip

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv nginx mysql-client -y

# Crear directorio del proyecto
sudo mkdir -p /var/www/lilis
sudo chown ubuntu:ubuntu /var/www/lilis
cd /var/www/lilis

# Clonar proyecto (o subir con scp)
git clone tu-repositorio.git .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# Configurar .env
nano .env
# Pegar configuración de producción

# Aplicar migraciones
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Paso 4: Configurar Gunicorn

Crear `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn daemon for Lilis Django
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/lilis
Environment="PATH=/var/www/lilis/venv/bin"
ExecStart=/var/www/lilis/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/lilis/gunicorn.sock \
          monitoreo.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Paso 5: Configurar Nginx

Crear `/etc/nginx/sites-available/lilis`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/lilis/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/lilis/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/lilis/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/lilis /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 6: Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## 🎯 OPCIÓN 3: AWS LIGHTSAIL (Más Económico)

### Ventajas:
- Precio fijo mensual ($5-$40)
- Más simple que EC2
- Incluye IP estática
- Ideal para proyectos pequeños/medianos

### Pasos:

1. Ir a Lightsail Console
2. Create Instance
3. Seleccionar "OS Only" → Ubuntu 22.04
4. Plan: $10/mes (1GB RAM, 40GB SSD)
5. Seguir pasos similares a EC2

---

## 📊 SERVICIOS AWS NECESARIOS

### Obligatorios:
- **EC2/EB/Lightsail**: Servidor de aplicación
- **RDS**: Base de datos MySQL
- **SES**: Envío de emails

### Recomendados:
- **S3**: Almacenamiento de archivos media
- **CloudFront**: CDN para archivos estáticos
- **ElastiCache**: Redis para caché
- **Route 53**: DNS
- **Certificate Manager**: SSL gratis

### Opcionales:
- **CloudWatch**: Monitoreo y logs
- **Backup**: Backups automáticos
- **WAF**: Firewall de aplicación web

---

## 💰 ESTIMACIÓN DE COSTOS MENSUALES

### Opción Económica (Lightsail):
- Lightsail $10/mes
- RDS db.t3.micro $15/mes
- SES $0 (primeros 62,000 emails gratis)
- **Total: ~$25/mes**

### Opción Estándar (EC2):
- EC2 t3.medium $30/mes
- RDS db.t3.small $25/mes
- S3 $5/mes
- SES $0
- **Total: ~$60/mes**

### Opción Escalable (Elastic Beanstalk):
- EB (2x t3.medium) $60/mes
- RDS db.t3.medium $50/mes
- ElastiCache $15/mes
- S3 + CloudFront $10/mes
- Load Balancer $20/mes
- **Total: ~$155/mes**

---

## 🔒 CONFIGURACIÓN DE SEGURIDAD

### 1. Configurar Security Groups

**EC2/EB Security Group:**
- SSH (22): Tu IP
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0

**RDS Security Group:**
- MySQL (3306): EC2 Security Group

### 2. Configurar IAM Roles

Crear rol para EC2/EB con permisos:
- AmazonSESFullAccess
- AmazonS3FullAccess
- CloudWatchLogsFullAccess

### 3. Habilitar backups automáticos

```bash
# Backup de RDS
aws rds modify-db-instance \
  --db-instance-identifier lilis-db \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00"
```

---

## 📝 VARIABLES DE ENTORNO PARA PRODUCCIÓN

```env
# Django
DJANGO_SECRET_KEY=genera-una-key-super-segura-de-50-caracteres
DJANGO_DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=.elasticbeanstalk.com,tudominio.com,www.tudominio.com

# Base de datos
DB_ENGINE=mysql
DB_NAME=lilis_production
DB_USER=admin
DB_PASSWORD=password_super_seguro_aqui
DB_HOST=lilis-db.xxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306

# Email (AWS SES)
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_SES_REGION=us-east-1
DEFAULT_FROM_EMAIL=noreply@tudominio.com

# Redis (ElastiCache)
REDIS_URL=redis://lilis-cache.xxxxx.0001.use1.cache.amazonaws.com:6379/0

# S3 (opcional)
AWS_STORAGE_BUCKET_NAME=lilis-media
AWS_S3_REGION_NAME=us-east-1
```

---

## ✅ CHECKLIST POST-DESPLIEGUE

- [ ] Aplicación accesible vía HTTP/HTTPS
- [ ] SSL configurado correctamente
- [ ] Base de datos conectada
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Archivos estáticos cargando
- [ ] Archivos media funcionando
- [ ] Emails enviándose correctamente
- [ ] Logs configurados
- [ ] Backups automáticos activos
- [ ] Monitoreo configurado
- [ ] Dominio apuntando correctamente
- [ ] Pruebas de carga realizadas

---

## 🚨 COMANDOS ÚTILES

```bash
# Ver logs en Elastic Beanstalk
eb logs

# SSH a instancia EB
eb ssh

# Actualizar aplicación
eb deploy

# Ver estado
eb status

# Escalar instancias
eb scale 3

# Reiniciar aplicación
eb restart

# Terminar entorno
eb terminate lilis-prod
```

---

## 📞 SOPORTE Y TROUBLESHOOTING

### Problema: 502 Bad Gateway
**Solución:** Verificar logs de Gunicorn y Nginx

### Problema: Archivos estáticos no cargan
**Solución:** Ejecutar `python manage.py collectstatic`

### Problema: Error de conexión a base de datos
**Solución:** Verificar Security Groups y endpoint de RDS

### Problema: Emails no se envían
**Solución:** Verificar dominio verificado en SES y credenciales

---

## 🎯 RECOMENDACIÓN FINAL

**Para este proyecto, recomiendo:**

1. **Elastic Beanstalk** para despliegue rápido y escalable
2. **RDS MySQL** para base de datos
3. **SES** para emails
4. **S3** para archivos media (opcional)
5. **CloudWatch** para monitoreo

**Costo estimado: $60-80/mes**

**Tiempo de despliegue: 2-3 horas**
