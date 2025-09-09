from django.contrib import admin
from .models import VeicoloInVendita, VeicoloImmagine

class VeicoloImmagineInline(admin.TabularInline):
    model = VeicoloImmagine
    extra = 1 # Numero di form vuoti da mostrare per le immagini della galleria
    fields = ('immagine', 'alt_text', 'ordine')

@admin.register(VeicoloInVendita)
class VeicoloInVenditaAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modello', 'anno', 'prezzo', 'chilometraggio', 'attivo', 'data_pubblicazione')
    list_filter = ('attivo', 'marca', 'tipo_carburante', 'tipo_cambio', 'trazione', 'anno')
    search_fields = ('marca', 'modello', 'descrizione')
    prepopulated_fields = {'slug': ('marca', 'modello', 'anno')} # Genera lo slug automaticamente
    inlines = [VeicoloImmagineInline] # Abilita l'aggiunta di immagini alla galleria
    fieldsets = (
        (None, {
            'fields': ('marca', 'modello', 'slug', 'anno', 'chilometraggio', 'prezzo', 'descrizione', 'attivo', 'is_quality')
        }),
        ('Specifiche Tecniche', {
            'fields': ('tipo_carburante', 'tipo_cambio', 'trazione', 'potenza_cv', 'cilindrata', 'numero_porte', 'numero_posti')
        }),
        ('Dettagli Estetici', {
            'fields': ('colore_esterno', 'colore_interno')
        }),
        ('Dotazione', {
            'fields': ('dotazione_opzionale',)
        }),
        ('Immagini', {
            'fields': ('foto_principale',)
        }),
    )