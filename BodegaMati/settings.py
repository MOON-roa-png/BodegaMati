# BodegaMati/settings.py
from pathlib import Path
import os
import dj_database_url
from django.core.management.utils import get_random_secret_key
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Seguridad / Entorno
# -----------------------------
# En local puedes dejar DEBUG=1. En Render pon DEBUG=0.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-" + get_random_secret_key())
DEBUG = os.environ.get("DEBUG", "1").lower() in ("1", "true", "yes")

# Hosts permitidos (separados por coma). En Render agrega tu dominio aquí o
# deja que se autoconfigure con RENDER_EXTERNAL_URL (ver abajo).
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()
]

# CSRF: orígenes confiables (con esquema). Agrega tu URL de Render si quieres,
# o deja que se autoconfigure más abajo.
_default_csrf = "http://localhost:8000,http://127.0.0.1:8000"
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", _default_csrf).split(",") if o.strip()
]

# Si Render define RENDER_EXTERNAL_URL (p.ej. https://tuapp.onrender.com)
# lo agregamos automáticamente a ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS.
_render_url = os.environ.get("RENDER_EXTERNAL_URL")
if _render_url:
    parsed = urlparse(_render_url)
    if parsed.hostname and parsed.hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(parsed.hostname)
    if _render_url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_render_url)

# Respeta X-Forwarded-Proto detrás de proxy (Render)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Forzar HTTPS opcional en prod (pon SECURE_SSL_REDIRECT=1 en Render si quieres)
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "0").lower() in ("1", "true", "yes")

# Cookies seguras cuando DEBUG=0
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# -----------------------------
# Apps
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bodega_app",
]

AUTH_USER_MODEL = "bodega_app.Usuario"
LOGIN_URL = "/usuarios/login/"
LOGIN_REDIRECT_URL = "/"

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para servir estáticos en producción
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "BodegaMati.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "BodegaMati.wsgi.application"

# -----------------------------
# Base de datos
# -----------------------------
# En despliegue: usa DATABASE_URL (Render te la da al crear el Postgres).
# En local: por defecto conecta al Postgres de tu máquina (5433), como ya usas.
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:postgres@localhost:5433/postgres",
        conn_max_age=600,
        ssl_require=False if DEBUG else True,
    )
}

# -----------------------------
# Password validators
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# i18n / tz
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------
# Archivos estáticos
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Django 5.x: STORAGES con WhiteNoise
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# -----------------------------
# Clave primaria por defecto
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
