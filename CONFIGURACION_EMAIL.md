# Configuración de Recuperación de Contraseña con Amazon SES

## Pasos para configurar el envío de correos en AWS Academy

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Amazon SES

#### En AWS Academy:
1. Ve al servicio **Amazon SES** en la consola de AWS
2. En el panel izquierdo, selecciona **Verified identities**
3. Haz clic en **Create identity**
4. Selecciona **Email address**
5. Ingresa tu email (ej: `tu-email@gmail.com`)
6. Haz clic en **Create identity**
7. **IMPORTANTE**: Revisa tu email y haz clic en el enlace de verificación

#### Configurar variables de entorno:
1. En AWS Academy, ve a **IAM** > **Users** > tu usuario
2. Ve a la pestaña **Security credentials**
3. Crea un **Access Key** si no tienes uno
4. Actualiza el archivo `.env`:

```env
# Cambiar DEBUG a False para usar SES
DJANGO_DEBUG=False

# Configuración de Amazon SES
AWS_ACCESS_KEY_ID=tu_access_key_de_aws_academy
AWS_SECRET_ACCESS_KEY=tu_secret_key_de_aws_academy
AWS_SES_REGION=us-east-1
DEFAULT_FROM_EMAIL=tu-email-verificado@gmail.com
```

### 3. Verificar configuración
```bash
python setup_ses.py
```

### 4. Probar la funcionalidad

1. Ejecuta el servidor:
```bash
python manage.py runserver
```

2. Ve a la página de login
3. Haz clic en "¿Olvidaste tu contraseña?"
4. Ingresa un email de un usuario existente
5. Revisa tu bandeja de entrada

### 5. Limitaciones en AWS Academy

- **Sandbox mode**: Solo puedes enviar emails a direcciones verificadas
- **Límites**: 200 emails por día, 1 email por segundo
- **Dominios**: Solo emails individuales, no dominios completos

### 6. Para producción real

Si quieres salir del sandbox mode (solo en cuentas AWS reales, no Academy):

1. Ve a SES > Account dashboard
2. Haz clic en "Request production access"
3. Completa el formulario explicando tu caso de uso

### 7. Solución de problemas

#### Error: "Email address not verified"
- Verifica que el email en `DEFAULT_FROM_EMAIL` esté verificado en SES

#### Error: "Access Denied"
- Verifica que las credenciales AWS sean correctas
- Asegúrate de que el usuario tenga permisos para SES

#### Error: "MessageRejected"
- Verifica que el email destinatario esté verificado (en sandbox mode)
- Revisa los límites de envío

### 8. Alternativa para desarrollo

Si tienes problemas con SES, puedes usar Gmail SMTP temporalmente:

```python
# En settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-app-password'  # No tu contraseña normal
```

**Nota**: Para Gmail necesitas generar una "App Password" en tu cuenta de Google.