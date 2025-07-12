# main/models.py
from django.db import models
from django.utils.text import slugify
 
 

class Servizio(models.Model):
    """
    Modello per rappresentare un servizio offerto dalla Carrozzeria Sangiorgio.
    """
    nome = models.CharField(max_length=200, verbose_name="Nome Servizio")
    slug = models.SlugField(unique=True, blank=True, help_text="Slug per URL puliti. Lascia vuoto per generare automaticamente.")
    descrizione_breve = models.TextField(verbose_name="Descrizione Breve", help_text="Breve descrizione per la lista servizi o homepage.")
    descrizione_completa = models.TextField(verbose_name="Descrizione Completa", help_text="Descrizione dettagliata per la pagina del servizio.")
    immagine_principale = models.ImageField(upload_to='servizi_immagini/', verbose_name="Immagine Principale", help_text="Immagine per la copertina del servizio.")
    icona_svg_code = models.TextField(
        blank=True,
        verbose_name="Codice SVG Icona",
        help_text="Codice SVG dell'icona del servizio (opzionale). In alternativa, usa le icone del tema."
    )
    ordine_visualizzazione = models.IntegerField(
        default=0,
        verbose_name="Ordine di Visualizzazione",
        help_text="Numero per ordinare i servizi (servizi con numero più basso vengono prima)."
    )
    attivo = models.BooleanField(default=True, verbose_name="Servizio Attivo", help_text="Indica se il servizio è visibile sul sito.")

    class Meta:
        verbose_name = "Servizio"
        verbose_name_plural = "Servizi"
        ordering = ['ordine_visualizzazione', 'nome'] # Ordina prima per numero, poi per nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


# NUOVO MODELLO PER I PUNTI CHIAVE
class PuntoChiaveServizio(models.Model):
    """
    Rappresenta un punto chiave o una caratteristica specifica di un servizio.
    Es: "Garanzia sul lavoro", "Materiali di alta qualità", etc.
    """
    servizio = models.ForeignKey(Servizio, related_name='punti_chiave', on_delete=models.CASCADE, verbose_name="Servizio di Riferimento")
    testo = models.CharField(max_length=255, verbose_name="Testo del Punto Chiave")
    ordine = models.PositiveIntegerField(default=0, verbose_name="Ordine di Visualizzazione")

    class Meta:
        verbose_name = "Punto Chiave del Servizio"
        verbose_name_plural = "Punti Chiave dei Servizi"
        ordering = ['ordine', 'testo']

    def __str__(self):
        return self.testo

# Modello per le immagini della galleria di un servizio (opzionale, per pagine di dettaglio)
class ServizioImmagine(models.Model):
    servizio = models.ForeignKey(Servizio, related_name='galleria_immagini', on_delete=models.CASCADE)
    immagine = models.ImageField(upload_to='servizi_galleria/')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Testo Alt Immagine")
    ordine = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordine']

    def __str__(self):
        return f"Immagine per {self.servizio.nome} ({self.id})"

# Modello per i membri del team (spostato da 'core' se non esisteva, o integrato)
class MembroTeam(models.Model):
    nome = models.CharField(max_length=100)
    ruolo = models.CharField(max_length=100)
    descrizione_breve = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    ordine = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Membro del Team"
        verbose_name_plural = "Membri del Team"
        ordering = ['ordine']

    def __str__(self):
        return self.nome
    
 

class FotoOfficina(models.Model):
    """
    Modello per rappresentare una singola foto della galleria dell'officina.
    """
    titolo = models.CharField(
        max_length=100, 
        help_text="Un titolo breve per la foto (es. 'La nostra cabina di verniciatura')."
    )
    descrizione = models.TextField(
        blank=True,
        help_text="Una descrizione opzionale per fornire maggiori dettagli sull'immagine."
    )
    foto = models.ImageField(
        upload_to='officina/',
        help_text="Carica l'immagine per la galleria."
    )
    ordine = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        help_text="Numero per ordinare le foto nella galleria (0 per primo)."
    )
    max_width = models.PositiveIntegerField(
        default=416,
        blank=True, 
        null=True,
        help_text="Opzionale: imposta una larghezza massima in pixel per questa immagine nella galleria. Utile per immagini panoramiche o più larghe."
    )

    class Meta:
        verbose_name = "Foto Officina"
        verbose_name_plural = "Foto Officina"
        ordering = ['ordine']

    def __str__(self):
        return self.titolo
    



class Certificazione(models.Model):
    nome = models.CharField(max_length=100)
    immagine = models.ImageField(upload_to='certificazioni/')
    
    ordine = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordine']
        verbose_name = "Certificazione"
        verbose_name_plural = "Certificazioni"

    def __str__(self):
        return self.nome
    

class Partner(models.Model):
    nome = models.CharField(max_length=100)
    immagine = models.ImageField(upload_to='partners/')
    ordine = models.PositiveIntegerField(default=0)
    in_homepage = models.BooleanField(default=False, verbose_name="Mostra in homepage")

    class Meta:
        ordering = ['ordine']
        verbose_name = "Partner"
        verbose_name_plural = "Partner"

    def __str__(self):
        return self.nome