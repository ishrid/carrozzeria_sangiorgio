import os
from .base import *
import dj_database_url

DEBUG = False

INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

ALLOWED_HOSTS = ['web-production-6298c6.up.railway.app', 'localhost', '127.0.0.1']

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}

# Nuova sintassi per Django 5+
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Sicurezza HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Leggi SECRET_KEY dalla variabile d'ambiente in produzione
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise Exception('DJANGO_SECRET_KEY non impostata!')