# GUÍA DE CONFIGURACIÓN DE EMAIL

## 📧 OPCIÓN 1: Gmail (Recomendado para Desarrollo)

### Paso 1: Habilitar "Contraseñas de Aplicación" en Gmail

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Selecciona "Seguridad" en el menú lateral
3. En "Cómo inicias sesión en Google", activa la "Verificación en dos pasos"
4. Una vez activada, busca "Contraseñas de aplicaciones"
5. Genera una nueva contraseña de aplicación:
   - Selecciona "Correo" como aplicación
   - Selecciona "Otro" como dispositivo
   - Escribe "Django Lilis"
   - Copia la contraseña generada (16 caracteres)

### Paso 2: Configurar el archivo .env

Edita tu archivo `.env` y actualiza estas líneas:

```env
# Activar envío real de emails
EMAIL_USE_REAL=True

# Configuración de Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # La contraseña de aplicación generada
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

### Paso 3: Probar el envío

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Prueba de Email',
    'Este es un email de prueba desde Django.',
    'tu_email@gmail.com',
    ['destinatario@example.com'],
    fail_silently=False,
)
```

---

## 📧 OPCIÓN 2: Outlook/Hotmail

### Configuración en .env:

```env
EMAIL_USE_REAL=True
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@outlook.com
EMAIL_HOST_PASSWORD=tu_contraseña
DEFAULT_FROM_EMAIL=tu_email@outlook.com
```

---

## 📧 OPCIÓN 3: Mailtrap (Para Testing)

Mailtrap es perfecto para desarrollo porque captura todos los emails sin enviarlos realmente.

### Paso 1: Crear cuenta en Mailtrap

1. Ve a https://mailtrap.io/
2. Crea una cuenta gratuita
3. Ve a tu inbox de prueba
4. Copia las credenciales SMTP

### Paso 2: Configurar .env

```env
EMAIL_USE_REAL=True
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=tu_username_mailtrap
EMAIL_HOST_PASSWORD=tu_password_mailtrap
DEFAULT_FROM_EMAIL=noreply@lilis.com
```

---

## 📧 OPCIÓN 4: AWS SES (Producción)

### Requisitos:
- Cuenta de AWS
- Dominio verificado
- Credenciales IAM con permisos SES

### Paso 1: Verificar dominio en AWS SES

1. Ve a AWS Console → SES
2. Verifica tu dominio o email
3. Crea usuario IAM con permisos SES
4. Genera Access Key y Secret Key

### Paso 2: Instalar dependencia

```bash
pip install django-ses
```

### Paso 3: Configurar .env

```env
DJANGO_DEBUG=False
EMAIL_USE_REAL=False  # SES se activa automáticamente en producción

AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_SES_REGION=us-east-1
DEFAULT_FROM_EMAIL=noreply@tudominio.com
```

---

## 🧪 PROBAR ENVÍO DE EMAILS

### Crear un usuario nuevo (enviará email automático):

```bash
python manage.py shell
```

```python
from usuarios.models import Usuario

# Crear usuario de prueba
usuario = Usuario.objects.create_user(
    username='test_email',
    email='tu_email_real@gmail.com',  # Usa tu email real
    password='temporal123',
    rol='LECTOR',
    estado='ACTIVO'
)

print("Usuario creado. Revisa tu email!")
```

### Cambiar contraseña (enviará email de notificación):

```python
usuario = Usuario.objects.get(username='test_email')
usuario.set_password('nueva_password123')
usuario.save()

print("Contraseña cambiada. Revisa tu email!")
```

---

## 🔍 VERIFICAR CONFIGURACIÓN

### Ver configuración actual:

```bash
python manage.py shell
```

```python
from django.conf import settings

print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'No configurado')}")
print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'No configurado')}")
print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'No configurado')}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
```

---

## ❌ SOLUCIÓN DE PROBLEMAS

### Error: "SMTPAuthenticationError"
**Causa:** Credenciales incorrectas o 2FA no configurado
**Solución:** 
- Verifica que usas contraseña de aplicación (no tu contraseña normal)
- Activa verificación en dos pasos en Gmail

### Error: "SMTPServerDisconnected"
**Causa:** Puerto o host incorrectos
**Solución:**
- Gmail: smtp.gmail.com:587
- Outlook: smtp-mail.outlook.com:587

### Error: "Connection refused"
**Causa:** Firewall o antivirus bloqueando
**Solución:**
- Desactiva temporalmente firewall
- Verifica que el puerto 587 esté abierto

### Los emails no llegan
**Causa:** Pueden estar en spam
**Solución:**
- Revisa carpeta de spam
- Agrega el remitente a contactos
- Usa Mailtrap para testing

---

## 📝 MODOS DE OPERACIÓN

### Modo 1: Desarrollo (Consola)
```env
EMAIL_USE_REAL=False
DJANGO_DEBUG=True
```
Los emails se muestran en la consola del servidor.

### Modo 2: Desarrollo (Gmail Real)
```env
EMAIL_USE_REAL=True
DJANGO_DEBUG=True
EMAIL_HOST_USER=tu_email@gmail.com
```
Los emails se envían realmente a través de Gmail.

### Modo 3: Testing (Mailtrap)
```env
EMAIL_USE_REAL=True
EMAIL_HOST=smtp.mailtrap.io
```
Los emails se capturan en Mailtrap sin envío real.

### Modo 4: Producción (AWS SES)
```env
DJANGO_DEBUG=False
AWS_ACCESS_KEY_ID=...
```
Los emails se envían a través de AWS SES.

---

## ✅ CHECKLIST DE CONFIGURACIÓN

- [ ] Cuenta de email configurada (Gmail/Outlook/Mailtrap)
- [ ] Contraseña de aplicación generada (si usas Gmail)
- [ ] Variables en .env actualizadas
- [ ] EMAIL_USE_REAL=True en .env
- [ ] Servidor Django reiniciado
- [ ] Prueba de envío realizada
- [ ] Email recibido correctamente

---

## 🎯 RECOMENDACIÓN

**Para desarrollo local:** Usa **Mailtrap** o **Gmail**
**Para producción:** Usa **AWS SES**

Mailtrap es ideal porque:
- No envía emails reales (evita spam)
- Interfaz web para ver emails
- Gratis hasta 500 emails/mes
- Perfecto para testing
