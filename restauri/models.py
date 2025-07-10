# restauri/models.py

from django.db import models
from django.utils.text import slugify

# ========= MODELLO PRINCIPALE DEL RESTAURO =========
# Questo modello rimane il cuore del progetto e non viene modificato significativamente.
# Contiene tutte le informazioni generali sul veicolo e sul lavoro svolto.

class Restauro(models.Model):
    TIPO_VEICOLO_CHOICES = [
        ('auto-epoca', "Auto d'Epoca"),
        ('moto', 'Moto'),
        ('progetti-speciali', 'Progetti Speciali'),
        ('altro', 'Altro'),
    ]

    titolo = models.CharField(max_length=255, verbose_name="Titolo del Progetto")
    slug = models.SlugField(unique=True, blank=True, help_text="Lascia vuoto per generare automaticamente dal titolo.")
    
    in_evidenza = models.BooleanField(default=False, verbose_name="In Evidenza", help_text="Seleziona per mostrare questo progetto nella sezione principale della pagina restauri.")

    marca_veicolo = models.CharField(max_length=100, verbose_name="Marca del Veicolo", blank=True)
    modello_veicolo = models.CharField(max_length=100, verbose_name="Modello del Veicolo", blank=True)
    anno_veicolo = models.IntegerField(verbose_name="Anno del Veicolo", blank=True, null=True)
    
    descrizione_breve = models.TextField(verbose_name="Descrizione Breve", help_text="Breve riassunto per le anteprime e l'introduzione.")
    descrizione_dettagliata = models.TextField(verbose_name="Descrizione Generale", help_text="Descrizione generale del progetto. I dettagli specifici andranno nelle singole 'Fasi di Lavoro'.", blank=True)
    
    foto_copertina = models.ImageField(
        upload_to='restauri/copertine/', 
        verbose_name="Immagine di Copertina",
        help_text="Immagine principale mostrata nelle liste e anteprime."
    )

    foto_prima = models.ImageField(upload_to='restauri/prima_dopo/', verbose_name="Foto Prima del Restauro", blank=True, null=True)
    foto_dopo = models.ImageField(upload_to='restauri/prima_dopo/', verbose_name="Foto Dopo il Restauro", blank=True, null=True)
    
    tipo_veicolo = models.CharField(max_length=50, choices=TIPO_VEICOLO_CHOICES, default='auto-epoca', verbose_name="Tipo di Progetto")
    
    data_completamento = models.DateField(verbose_name="Data Completamento Progetto", blank=True, null=True)
    ordine_visualizzazione = models.IntegerField(default=0, verbose_name="Ordine di Visualizzazione", help_text="Numero per ordinare i progetti (più basso = prima).")
    attivo = models.BooleanField(default=True, verbose_name="Visibile sul Sito")

    class Meta:
        verbose_name = "Progetto di Restauro"
        verbose_name_plural = "Progetti di Restauro"
        ordering = ['ordine_visualizzazione', '-data_completamento']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titolo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titolo


# ========= NUOVI MODELLI PER LE FASI DI LAVORO DETTAGLIATE =========
# Sostituiscono il vecchio modello "RestauroImmagine" per permettere una narrazione
# strutturata del processo di restauro.

class FaseLavoro(models.Model):
    """
    Rappresenta una singola fase del processo di restauro (es. Lattoneria, Verniciatura).
    Ogni restauro può avere molteplici fasi.
    """
    restauro = models.ForeignKey(Restauro, on_delete=models.CASCADE, related_name='fasi_lavoro', verbose_name="Progetto di Riferimento")
    titolo = models.CharField(max_length=200, verbose_name="Titolo della Fase", help_text="Es: 'Smontaggio e Lattoneria', 'Verniciatura', 'Restauro Interni'")
    descrizione = models.TextField(verbose_name="Descrizione Attività Svolte", blank=True)
    ordine = models.PositiveIntegerField(default=0, verbose_name="Ordine di Visualizzazione", help_text="Per ordinare le fasi cronologicamente (0, 1, 2...).")

    class Meta:
        verbose_name = "Fase di Lavoro"
        verbose_name_plural = "Fasi di Lavoro"
        ordering = ['ordine']

    def __str__(self):
        return f"{self.restauro.titolo} - Fase: {self.titolo}"


class ImmagineFase(models.Model):
    """
    Rappresenta una singola immagine all'interno di una specifica FaseLavoro.
    Ogni fase può avere la sua galleria di immagini.
    """
    fase = models.ForeignKey(FaseLavoro, on_delete=models.CASCADE, related_name='immagini_fase', verbose_name="Fase di Riferimento")
    immagine = models.ImageField(upload_to='restauri/fasi/', verbose_name="Immagine")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Testo Alternativo (SEO)", help_text="Breve descrizione dell'immagine per l'accessibilità e i motori di ricerca.")
    ordine = models.PositiveIntegerField(default=0, verbose_name="Ordine Immagine")

    class Meta:
        verbose_name = "Immagine della Fase"
        verbose_name_plural = "Immagini della Fase"
        ordering = ['ordine']

    def __str__(self):
        return f"Immagine per la fase '{self.fase.titolo}'"

# NOTA: Il modello "RestauroImmagine" è stato rimosso e sostituito 
# dalla combinazione di "FaseLavoro" e "ImmagineFase" per una maggiore flessibilità.