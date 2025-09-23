"""
Django settings for BodegaMati project.
"""
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Seguridad
# =========================
SECRET_KEY = config("DJANGO_SECRET_KEY", default="insecure-key")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:8000,http://127.0.0.1:8000"
).split(",")

# Respeta HTTPS detrás del proxy (Render, etc.)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# =========================
# Apps instaladas
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bodega_app',
]

AUTH_USER_MODEL = 'bodega_app.Usuario'

# =========================
# Auth redirects
# =========================
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'  # <-- agregado

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BodegaMati.urls'

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Si tenés carpeta global /templates, agregala aquí
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

WSGI_APPLICATION = 'BodegaMati.wsgi.application'
ASGI_APPLICATION = 'BodegaMati.asgi.application'

# =========================
# Base de datos (Render)
# =========================
DATABASES = {
    'default': dj_database_url.parse(
        config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# =========================
# Validación de contraseñas
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# Internacionalización
# =========================
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Asuncion'
USE_I18N = True
USE_TZ = True

# =========================
# Archivos estáticos
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================
# Default primary key field
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
