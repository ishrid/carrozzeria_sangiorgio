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
    Abbiamo sostituito il vecchio inline con quello nuovo per le Fasi di Lavoro.
    """
    list_display = ('titolo', 'tipo_veicolo', 'in_evidenza', 'attivo', 'data_completamento', 'ordine_visualizzazione')
    list_filter = ('attivo', 'in_evidenza', 'tipo_veicolo')
    search_fields = ('titolo', 'marca_veicolo', 'modello_veicolo')
    prepopulated_fields = {'slug': ('titolo',)}
    
    # Sostituiamo il vecchio inline con quello nuovo
    inlines = [FaseLavoroInline] 
    inlines = [RestauroImmagineInline] # Abilita l'aggiunta di immagini alla galleria
    
    # I fieldset rimangono quasi identici, sono ben organizzati
    fieldsets = (
        (None, {
            'fields': ('titolo', 'slug', 'in_evidenza', 'attivo', 'descrizione_breve', 'descrizione_dettagliata')
        }),
        ('Dettagli Veicolo', {
            'fields': ('marca_veicolo', 'modello_veicolo', 'anno_veicolo', 'tipo_veicolo', 'data_completamento')
        }),
        ('Immagini Principali', {
            'fields': ('foto_copertina', 'foto_prima', 'foto_dopo')
        }),
        ('Ordinamento', {
            'fields': ('ordine_visualizzazione',)
        }),
    )

@admin.register(FaseLavoro)
class FaseLavoroAdmin(admin.ModelAdmin):
    """
    Configurazione dedicata per il modello 'FaseLavoro'.
    Questa vista permette di gestire i dettagli di una fase e di CARICARE LE IMMAGINI
    grazie all'inline 'ImmagineFaseInline'.
    """
    list_display = ('titolo', 'restauro', 'ordine')
    list_filter = ('restauro__titolo',) # Filtra per titolo del restauro a cui appartiene
    search_fields = ('titolo', 'descrizione')
    
    # Qui inseriamo l'inline per le immagini!
    inlines = [ImmagineFaseInline]
    
    fieldsets = (
        (None, {
            'fields': ('restauro', 'titolo', 'ordine', 'descrizione')
        }),
    )

# NOTA: Non è necessario registrare 'ImmagineFase' direttamente,
# perché viene già gestito tramite l'inline dentro 'FaseLavoroAdmin'. 