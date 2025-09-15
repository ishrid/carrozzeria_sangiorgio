from django.db import models
from django.utils.text import slugify

class VeicoloInVendita(models.Model):
    """
    Modello per rappresentare un veicolo disponibile per la vendita.
    """
    TIPO_CARBURANTE_CHOICES = [
        ('benzina', 'Benzina'),
        ('diesel', 'Diesel'),
        ('elettrico', 'Elettrico'),
        ('ibrido', 'Ibrido'),
        ('gpl', 'GPL'),
        ('metano', 'Metano'),
    ]

    TIPO_CAMBIO_CHOICES = [
        ('manuale', 'Manuale'),
        ('automatico', 'Automatico'),
    ]

    TRAZIONE_CHOICES = [
        ('anteriore', 'Anteriore'),
        ('posteriore', 'Posteriore'),
        ('integrale', 'Integrale'),
    ]

    STATUS_CHOICES = [
        ('disponibile', 'Disponibile'),
        ('trattativa', 'In Trattativa'),
        ('venduto', 'Venduto'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponibile')
    

    marca = models.CharField(max_length=100, verbose_name="Marca")
    modello = models.CharField(max_length=100, verbose_name="Modello")
    slug = models.SlugField(unique=True, blank=True, help_text="Slug per URL puliti. Lascia vuoto per generare automaticamente.")
    anno = models.IntegerField(verbose_name="Anno di Immatricolazione")
    chilometraggio = models.CharField(verbose_name="Chilometraggio (Km)")
    prezzo = models.CharField(max_length=100, verbose_name="Prezzo (CHF)")
    descrizione = models.TextField(verbose_name="Descrizione del Veicolo", blank=True, null=True)
    consumo_totale = models.CharField(max_length=100, verbose_name="Consumo totale", blank=True,null=True)
    marce = models.CharField(max_length=100, verbose_name="Marce", blank=True,null=True) 
    
 
    
    
    
    tipo_carburante = models.CharField(max_length=50, choices=TIPO_CARBURANTE_CHOICES, verbose_name="Tipo Carburante")
    tipo_cambio = models.CharField(max_length=50, choices=TIPO_CAMBIO_CHOICES, verbose_name="Tipo Cambio")
    trazione = models.CharField(max_length=50, choices=TRAZIONE_CHOICES, verbose_name="Trazione")
    tipo_veicolo = models.CharField(max_length=50, verbose_name="Tipo veicolo", blank=True)
    colore = models.CharField(max_length=50, verbose_name="Colore", blank=True, null=True)
    
    numero_porte = models.IntegerField(verbose_name="Numero Porte", blank=True, null=True)
    numero_posti = models.IntegerField(verbose_name="Numero Posti", blank=True, null=True)
    potenza_cv = models.IntegerField(verbose_name="Potenza (CV)", blank=True, null=True)
    cilindrata = models.CharField(verbose_name="Cilindrata", blank=True, null=True)


    tit1 = models.CharField(verbose_name="Motore e trasmissione", default="Motore e trasmissione", blank=True, null=True)
    box1 = models.TextField(verbose_name="Box 1", blank=True, null=True)
    
    tit2 = models.CharField(verbose_name="Prestazioni e consumi", default="Prestazioni e consumi", blank=True, null=True)
    box2 = models.TextField(verbose_name="Box 2", blank=True, null=True)
    

    tit3 = models.CharField(verbose_name="Comfort, sicurezza e altre dotazioni", default="Comfort, sicurezza e altre dotazioni", blank=True, null=True)
    box3 = models.TextField(verbose_name="Box 3", blank=True, null=True)
    
    
    
    
    # Dotazione opzionale (può essere un JSONField per maggiore flessibilità o TextField per una lista semplice)
    dotazione_opzionale = models.TextField(
        blank=True,
        verbose_name="Dotazione Opzionale",
        help_text="Lista di optional separati da virgole o newline."
    )
    
    foto_principale = models.ImageField(upload_to='veicoli_vendita/', verbose_name="Foto Principale")
    
    data_pubblicazione = models.DateTimeField(auto_now_add=True, verbose_name="Data di Pubblicazione")
    attivo = models.BooleanField(default=True, verbose_name="Disponibile per la Vendita")
    is_quality = models.BooleanField(default=False, verbose_name="quality?")

    class Meta:
        verbose_name = "Veicolo in Vendita"
        verbose_name_plural = "Veicoli in Vendita"
        ordering = ['-data_pubblicazione'] # Ordina dal più recente

    def save(self, *args, **kwargs):
        if not self.slug:
            # Combina marca, modello e anno per uno slug più unico
            self.slug = slugify(f"{self.marca}-{self.modello}-{self.anno}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.anno})"

class VeicoloImmagine(models.Model):
    """
    Modello per le immagini della galleria di un veicolo in vendita.
    """
    veicolo = models.ForeignKey(VeicoloInVendita, related_name='galleria_foto', on_delete=models.CASCADE)
    immagine = models.ImageField(upload_to='veicoli_galleria/')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Testo Alt Immagine")
    ordine = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordine']
        verbose_name = "Immagine Veicolo"
        verbose_name_plural = "Immagini Veicolo"

    def __str__(self):
        return f"Immagine per {self.veicolo.marca} {self.veicolo.modello} ({self.id})"