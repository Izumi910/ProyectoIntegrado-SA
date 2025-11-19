from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass  # Continue if .env file doesn't exist

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or "dev-secret"
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"


ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'django_ratelimit',
    'productos',
    'usuarios', 
    'proveedores',
    'inventario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'usuarios.middleware.SingleSessionMiddleware',  # Prevenir múltiples sesiones
    'usuarios.middleware.SecurityMiddleware',  # Validaciones de seguridad
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitoreo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitoreo.wsgi.application'


# Database - Compatible con AWS RDS
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
    # Configuración automática para AWS RDS (Elastic Beanstalk)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'connect_timeout': 10,
            },
        }
    }
else:
    # Configuración manual con variables de entorno
    ENGINE = os.getenv("DB_ENGINE", "sqlite")
    
    if ENGINE == "mysql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("DB_NAME"),
                "USER": os.getenv("DB_USER"),
                "PASSWORD": os.getenv("DB_PASSWORD"),
                "HOST": os.getenv("DB_HOST", "localhost"),
                "PORT": os.getenv("DB_PORT", "3306"),
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }
    elif ENGINE == "postgresql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("DB_NAME"),
                "USER": os.getenv("DB_USER"),
                "PASSWORD": os.getenv("DB_PASSWORD"),
                "HOST": os.getenv("DB_HOST", "localhost"),
                "PORT": os.getenv("DB_PORT", "5432"),
            }
        }
    else:  # SQLite por defecto
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
            }
        }

# Cache configuration for django_ratelimit
if DEBUG:
    # Para desarrollo - desactiva el rate limiting
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    # Para producción - usar Redis
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# WhiteNoise configuration
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usuarios.Usuario'

LOGIN_REDIRECT_URL = 'usuarios:dashboard'

LOGIN_URL = 'usuarios:login'

LOGOUT_REDIRECT_URL = 'login'





# Configuraciones de sesión

# duración de la cookie de sesión (en segundos)
SESSION_COOKIE_AGE = 60*60*2 # 2 horas 
# sesión expira al cerrar el navegador?
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# cada vez que se hace una petición, se actualiza la expiración
SESSION_SAVE_EVERY_REQUEST = False
# seguridad de las cookies
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'

# Configuraciones de seguridad avanzadas
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Desactivar forzamiento HTTPS y HSTS en desarrollo
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'security.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Configuración de Email
EMAIL_USE_REAL = os.getenv('EMAIL_USE_REAL', 'False') == 'True'

if EMAIL_USE_REAL:
    # Configuración para Gmail (desarrollo)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # tu_email@gmail.com
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # contraseña de aplicación
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
elif not DEBUG:
    # Para producción con Amazon SES
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION', 'us-east-1')
    AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@lilis.com')
else:
    # Desarrollo - mostrar en consola
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@lilis.com')
