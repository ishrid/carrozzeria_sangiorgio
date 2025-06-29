# carrozzeria_sangiorgio/settings/dev.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database SQLite locale per sviluppo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Usa il backend default di Django per file media (locale)
# NON serve sovrascrivere DEFAULT_FILE_STORAGE qui
