from .base import *
import dj_database_url
import os
from datetime import timedelta

# ------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

APPEND_SLASH = True

# ------------------------------------------------------------
# BASE DE DATOS
# ------------------------------------------------------------
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
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# ------------------------------------------------------------
# REST FRAMEWORK + JWT
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
# LOGGING
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
# ARCHIVOS ESTÁTICOS / MEDIA
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
