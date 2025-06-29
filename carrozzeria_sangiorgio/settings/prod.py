# carrozzeria_sangiorgio/settings/prod.py

import os
from .base import *
import dj_database_url

DEBUG = False

# Aggiungi qui le app Cloudinary!
# È essenziale che queste siano in INSTALLED_APPS per funzionare.
INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

# IMPORTANTE: Aggiorna questo con l'URL effettivo della tua app Railway
# Lo troverai nella dashboard di Railway dopo il primo deployment.
ALLOWED_HOSTS = ['your-railway-app-name.up.railway.app', 'localhost', '127.0.0.1']

# Database configuration for Railway
# Railway inietta automaticamente DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Cloudinary settings
# Prese dalle variabili d'ambiente di Railway
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}

# Imposta Cloudinary come storage predefinito per media e statici in produzione
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

# STATIC_ROOT deve essere definito per collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings per HTTPS in produzione
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Potresti voler aggiungere:
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_HSTS_SECONDS = 31536000 # 1 anno
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# La SECRET_KEY deve essere letta da variabile d'ambiente in produzione
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')