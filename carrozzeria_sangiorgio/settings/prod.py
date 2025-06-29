
# .env

# carrozzeria_sangiorgio/settings/prod.py

import os
from .base import *
import dj_database_url

DEBUG = False

# IMPORTANTE: Aggiungi qui le app Cloudinary!
INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

# Aggiungi l'URL effettivo della tua applicazione Railway quando la creerai
ALLOWED_HOSTS = ['your-railway-app-name.up.railway.app', 'localhost', '127.0.0.1']

# Database configuration for Railway
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

# Static files (CSS, JavaScript, images)
# Assicurati che STATIC_ROOT sia impostato per collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles' # Molto importante per collectstatic

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Potrebbe essere necessario configurare SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, SECURE_HSTS_PRELOAD
# a seconda delle tue esigenze di sicurezza. Inizia con questi e poi espandi.

# Secret Key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')