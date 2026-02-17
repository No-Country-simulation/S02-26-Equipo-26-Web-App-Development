from pathlib import Path
import os
import environ
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# ENV
# =========================

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# =========================
# SECURITY
# =========================

SECRET_KEY = env("DJANGO_SECRET_KEY", default="unsafe-secret")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    'rest_framework_simplejwt',
    # Local apps
    'apps.users',
    'apps.patients',
    'apps.caregivers',
    'apps.admins',
    'apps.documents',
    'apps.payments',
    'apps.shifts',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'apps.users.middleware.JWTAuthenticationMiddleware',
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# =========================
# DATABASE (POSTGRES)
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# REST Framework 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
SIMPLE_JWT = {    
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),    
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    
    'ROTATE_REFRESH_TOKENS': True,    
    'BLACKLIST_AFTER_ROTATION': True,    
    'ALGORITHM': 'HS256',    
    'SIGNING_KEY': env('DJANGO_SECRET_KEY'),    
    'AUTH_HEADER_TYPES': ('Bearer',),    
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',    
    'USER_ID_FIELD': 'id',    
    'USER_ID_CLAIM': 'user_id',}

# Custom User Model
AUTH_USER_MODEL = 'users.User'


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Email Configuration (Para que funcionen los signals)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_USER', default='tu-email@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@cuidadores.com')

# Configuración de Jazzmin (tema moderno para admin)
JAZZMIN_SETTINGS = {    
    "site_title": "Cuidadores Admin",    
    "site_header": "Sistema de Gestión",   
    "site_brand": "Cuidadores",   
    "welcome_sign": "Bienvenido al Panel de Administración", 
    "copyright": "Tu Empresa PYME",
    }

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

# =========================
# STATIC
# =========================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
