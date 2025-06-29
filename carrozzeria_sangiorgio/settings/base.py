# carrozzeria_sangiorgio/settings/base.py

import os
from pathlib import Path
from dotenv import load_dotenv # Aggiungi questa riga

load_dotenv() # Carica le variabili da .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Legge la SECRET_KEY dal .env per lo sviluppo, come preferisci.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-insecure-key-if-not-set')

# DEBUG è gestito nei file dev.py e prod.py
ALLOWED_HOSTS = [] # Questo è gestito nei file dev.py e prod.py

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Lascia SOLO questo per gli statici
    'main',
    # Rimuovi completamente le seguenti righe se erano qui:
    # 'cloudinary_storage',
    # 'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'carrozzeria_sangiorgio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # Lascia a True per trovare i template delle app Django
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'carrozzeria_sangiorgio.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Impostazioni per i MEDIA files (immagini dei post - LOCALE)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directory locale per i media

# Impostazioni per i STATIC files (CSS, JS, immagine di copertina - LOCALE)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Directory locale per collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Dove cerchi i tuoi statici personalizzati
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' # Usa lo storage predefinito di Django

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'