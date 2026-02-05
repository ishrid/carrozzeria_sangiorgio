# restauri/admin.py

from django.contrib import admin
from .models import Restauro, FaseLavoro, ImmagineFase , RestauriImmagine# ✅ 1. Importiamo i nuovi modelli

# =============================================================================
# ✅ 2. CREIAMO GLI "INLINE" PER LA GESTIONE annidata
# =============================================================================
class RestauroImmagineInline(admin.TabularInline):
    model = RestauriImmagine
    extra = 1 # Numero di form vuoti da mostrare per le immagini della galleria
    fields = ('immagine', 'alt_text', 'ordine')

class ImmagineFaseInline(admin.TabularInline):
    """
    Questo permette di aggiungere immagini DIRETTAMENTE dentro una FaseLavoro.
    """
    model = ImmagineFase
    extra = 1 # Mostra 1 campo vuoto per caricare una nuova immagine
    fields = ('immagine', 'alt_text', 'ordine')
    verbose_name = "Immagine"
    verbose_name_plural = "Galleria Immagini per questa Fase"


class FaseLavoroInline(admin.TabularInline):
    """
    Questo permette di aggiungere le Fasi di Lavoro DIRETTAMENTE dentro un Restauro.
    Mostra solo i campi principali per non affollare la pagina.
    """
    model = FaseLavoro
    extra = 1 # Mostra 1 campo vuoto per creare una nuova fase
    fields = ('titolo', 'descrizione', 'ordine')
    verbose_name = "Fase di Lavoro"
    verbose_name_plural = "Fasi di Lavoro del Progetto"


# =============================================================================
# ✅ 3. REGISTRIAMO I MODELLI NELL'AREA ADMIN
# =============================================================================

@admin.register(Restauro)
class RestauroAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello principale 'Restauro'.
    """

    list_display = (
        'titolo',
        'tipo_veicolo',
        'marca_veicolo',
        'modello_veicolo',
        'in_evidenza',
        'attivo',
        'data_completamento',
        'ordine_visualizzazione'
    )

    list_filter = ('attivo', 'in_evidenza', 'tipo_veicolo')
    search_fields = ('titolo', 'marca_veicolo', 'modello_veicolo')
    prepopulated_fields = {'slug': ('titolo',)}

    # ✅ ENTRAMBI GLI INLINE
    inlines = [
         
        RestauroImmagineInline
    ]

    fieldsets = (
        (None, {
            'fields': (
                'titolo',
                'slug',
                'in_evidenza',
                'attivo',
                'descrizione_breve',
                 
            )
        }),

        ('Dettagli Veicolo', {
            'fields': (
                'marca_veicolo',
                'modello_veicolo',
                'anno_veicolo',
                'versione_veicolo',
                'tipo_veicolo',
                'data_completamento'
            )
        }),

        # 🔧 NUOVO BLOCCO TECNICO
        ('Specifiche Tecniche', {
            
            'fields': (
                'freni',
                'sospensioni',
                'velocita_massima',
                'peso',
                'dimensioni',
                'cilindrata',
                'carrozzeria',
                'motore',
                'trasmissione',
                'potenza_massima',
                'trazione'

            )
        }),

        ('Immagini Principali', {
            'fields': (
                'logo_macchina',
                'foto_copertina',
                'foto_prima',
                'foto_dopo'
            )
        }),

        ('Ordinamento', {
            'fields': ('ordine_visualizzazione',)
        }),
    )
