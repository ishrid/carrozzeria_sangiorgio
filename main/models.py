# main/models.py
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titolo")
    content = models.TextField(verbose_name="Contenuto")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Data di Pubblicazione")
    # Aggiungi questa riga per l'immagine
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Immagine")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title