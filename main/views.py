# main/views.py
from django.shortcuts import render
from .models import Post # Importa il modello Post

def home(request):
    # Recupera tutti i post dal database, ordinati per data (dal più recente)
    # Limita ad esempio agli ultimi 3 post per la copertina
    posts = Post.objects.all()[:3] # Prendi gli ultimi 3 post

    context = {
        'posts': posts # Passa la lista dei post al template
    }
    return render(request, 'index.html', context)