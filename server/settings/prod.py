from .base import *
import dj_database_url
import os

DEBUG = False

# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Configuración CORS
CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend.com",
    "https://www.tu-frontend.com",
]

# Protección CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://tu-frontend.com",
    "https://www.tu-frontend.com",
]

# Configuraciones de seguridad adicionales
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

