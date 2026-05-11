"""
Django settings for SkyApp project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-r&s*^vvesg9!7h#w8jf2kcfab9v#@y+xkaf-5ae@0=r$p5mabl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "skyapp.skyconnect-sa.com",
    "localhost",
    "127.0.0.1",
    "10.7.1.187",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # vos apps
    "clients",
    "techniciens",
    "commercials",
    "activites",
    "rapportActivites",
    "billing",
    "base_stations",
    "type_contrats",
    "users",
    "prospects",
    "employes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.LastUserActivityMiddleware",
]

ROOT_URLCONF = "SkyApp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "clients.context_processors.role_user",
            ],
        },
    },
]

WSGI_APPLICATION = "SkyApp.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "skyapp",
        "USER": "skyuser",
        "PASSWORD": "skypass",
        "HOST": "db",
        "PORT": 5432,
    }
}

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files (pour les uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Créer le dossier media si nécessaire
os.makedirs(MEDIA_ROOT / "technicien/photos", exist_ok=True)

# Configuration de l'authentification
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "users:login"

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Session
SESSION_COOKIE_AGE = 3600  # 1 heure
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "sckyconnect@gmail.com"
EMAIL_HOST_PASSWORD = "ybdb bnrg lxpe qcmq"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============ CONFIGURATION CSRF CORRIGÉE ============

# Configuration de base CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://skyapp.skyconnect-sa.com",
    "http://skyapp.skyconnect-sa.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Configuration des cookies CSRF et Session
# IMPORTANT: Pour le développement local sans HTTPS
CSRF_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
SESSION_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS

# Paramètres additionnels pour résoudre l'erreur CSRF
CSRF_COOKIE_HTTPONLY = False  # Permet à JavaScript d'accéder au cookie si nécessaire
CSRF_COOKIE_SAMESITE = "Lax"  # Équilibrer sécurité et fonctionnalité
CSRF_USE_SESSIONS = False  # Utiliser les cookies par défaut

# Pour s'assurer que le cookie est bien défini
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Configuration pour les sessions (si vous utilisez des sessions basées sur cache)
# Supprimer la configuration conditionnelle qui pourrait causer des problèmes
SESSION_ENGINE = (
    "django.contrib.sessions.backends.db"  # Utiliser la base de données par défaut
)

# Configuration cache (optionnelle, seulement si nécessaire)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
