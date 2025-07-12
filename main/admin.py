# main/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Servizio, ServizioImmagine, MembroTeam, FotoOfficina, Certificazione, Partner, PuntoChiaveServizio


class PuntoChiaveServizioInline(admin.TabularInline):
    model = PuntoChiaveServizio
    fields = ['testo', 'ordine'] # Campi da mostrare per ogni punto chiave
    extra = 1 # Mostra uno slot vuoto per aggiungere un nuovo punto chiave
    verbose_name = "Punto Chiave"
    verbose_name_plural = "Punti Chiave del Servizio"


class ServizioImmagineInline(admin.TabularInline):
    model = ServizioImmagine
    extra = 1 # Numero di form vuoti da mostrare

@admin.register(Servizio)
class ServizioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'attivo', 'ordine_visualizzazione')
    list_filter = ('attivo',)
    search_fields = ('nome', 'descrizione_breve')
    prepopulated_fields = {'slug': ('nome',)} # Genera lo slug automaticamente dal nome
    inlines = [PuntoChiaveServizioInline, ServizioImmagineInline] # Abilita l'aggiunta di immagini alla galleria direttamente dal form del servizio

@admin.register(MembroTeam)
class MembroTeamAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ruolo', 'ordine')
    list_editable = ('ordine',)
    search_fields = ('nome', 'ruolo')


# In main/admin.py



# Crea una classe di amministrazione personalizzata per il tuo modello
@admin.register(FotoOfficina)
class FotoOfficinaAdmin(admin.ModelAdmin):
    
    # 1. MOSTRARE PIÙ INFORMAZIONI NELL'ELENCO
    # Mostra una anteprima dell'immagine, il titolo e l'ordine direttamente nella lista.
    list_display = ('mostra_thumbnail', 'titolo', 'ordine', 'max_width')

    list_editable = ('ordine','max_width')
    
    # 2. AGGIUNGERE CAMPI DI RICERCA
    # Permette di cercare le foto per titolo e descrizione.
    search_fields = ('titolo', 'descrizione')
    
    # 3. ORGANIZZARE I CAMPI NELLA PAGINA DI MODIFICA
    # Raggruppa i campi in sezioni logiche per una maggiore chiarezza.
    fieldsets = (
        ('Informazioni Principali', {
            'fields': ('titolo', 'descrizione', 'foto', 'mostra_anteprima_grande')
        }),
        ('Impostazioni di Visualizzazione', {
            'fields': ('ordine', 'max_width')
        }),
    )
    
    # 4. MOSTRARE L'ANTEPRIMA DELL'IMMAGINE ANCHE NELLA PAGINA DI MODIFICA
    # Definisce i campi che sono "solo lettura" (non modificabili).
    readonly_fields = ('mostra_anteprima_grande',)

    # --- Metodi personalizzati per le anteprime ---

    def mostra_thumbnail(self, obj):
        """
        Crea un piccolo thumbnail per la vista elenco (list_display).
        """
        if obj.foto:
            return format_html(f'<img src="{obj.foto.url}" style="height: 60px; border-radius: 5px;" />')
        return "Nessuna Immagine"
    mostra_thumbnail.short_description = 'Anteprima'

    def mostra_anteprima_grande(self, obj):
        """
        Crea un'anteprima più grande per la vista di dettaglio (fieldsets).
        """
        if obj.foto:
            return format_html(f'<img src="{obj.foto.url}" style="max-height: 300px; border-radius: 5px;" />')
        return "Nessuna Immagine"
    mostra_anteprima_grande.short_description = 'Anteprima Immagine Caricata'

 

@admin.register(Certificazione)
class CertificazioneAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordine')
    ordering = ('ordine',)



@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordine', 'in_homepage')
    list_filter = ('in_homepage',)
    ordering = ('ordine',)