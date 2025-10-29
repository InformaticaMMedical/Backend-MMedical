from .base import *
import dj_database_url
import os
from datetime import timedelta

# ------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------
# BASE DE DATOS
# ------------------------------------------------------------
# En desarrollo, normalmente no forzamos SSL y usamos SQLite o Postgres local.
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}
# ------------------------------------------------------------
# CORS / CSRF
# ------------------------------------------------------------
# Permitir peticiones desde el frontend de desarrollo (React + Vite)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",  # a veces Vite usa esta URL
]

# O, si quieres permitir todo (solo en desarrollo)
CORS_ALLOW_ALL_ORIGINS = True

# Para que las peticiones con token funcionen bien
CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------------------
# REST FRAMEWORK + JWT (por claridad)
# ------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "usuarios.authentication.CookieJWTAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ------------------------------------------------------------
# LOGGING (opcional, útil en dev)
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# ------------------------------------------------------------
# ARCHIVOS ESTÁTICOS (para servir en dev)
# ------------------------------------------------------------
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------------------------------------
# SUPABASE STORAGE
# ------------------------------------------------------------
SUPABASE_STORAGE_URL = os.getenv("SUPABASE_STORAGE_URL")
SUPABASE_PUBLIC_BASE = os.getenv("SUPABASE_PUBLIC_BASE")
SUPABASE_REGION = os.getenv("SUPABASE_REGION", "us-east-2")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "imagenes")
SUPABASE_ACCESS_KEY = os.getenv("SUPABASE_ACCESS_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
