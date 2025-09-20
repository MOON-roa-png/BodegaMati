# BodegaMati/settings.py
from pathlib import Path
import os
import dj_database_url  # <-- lee DATABASE_URL en despliegue

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Seguridad / Entorno
# -----------------------------
# Usa variables de entorno en producción. En local puedes dejar DEBUG=1.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-key-change-me")
DEBUG = os.environ.get("DEBUG", "1") in ("1", "true", "True")

# Hosts permitidos (separa por comas). En Render/Railway setea tu dominio aquí.
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]

# CSRF: orígenes confiables (con esquema) para panel y formularios.
# Ej: "https://tuapp.onrender.com,https://midominio.com"
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost:8000").split(",") if o.strip()
]

# Si estás detrás de proxy (Render/Railway) confía en X-Forwarded-Proto para HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies seguras en prod
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
# En despliegue: usa DATABASE_URL (Render/Railway te lo da).
# En local: cae al Postgres que ya tienes (localhost:5433).
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

# En Django 5.x usa STORAGES para WhiteNoise
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# -----------------------------
# Clave primaria por defecto
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
