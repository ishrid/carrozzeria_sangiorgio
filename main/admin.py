# main/admin.py
from django.contrib import admin
from .models import Post # Importa il tuo modello Post

# Registra il tuo modello qui.
admin.site.register(Post)