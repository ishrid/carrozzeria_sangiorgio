# restauri/views.py

from django.shortcuts import render, get_object_or_404
from .models import Restauro

def restauri_list_view(request):
    """
    Visualizza la lista dei progetti di restauro con una sezione "In Evidenza"
    e una griglia filtrabile per tutti gli altri.
    """
    # Recupera i progetti da mostrare nella sezione "In Evidenza"
    restauri_in_evidenza = Restauro.objects.filter(attivo=True, in_evidenza=True)

    # Recupera tutti gli altri progetti attivi per la griglia
    tutti_i_restauri = Restauro.objects.filter(attivo=True)
    
    context = {
        'restauri_in_evidenza': restauri_in_evidenza,
        'restauri': tutti_i_restauri,
        'tipi_veicolo': Restauro.TIPO_VEICOLO_CHOICES, # Per popolare i bottoni del filtro
    }
    return render(request, 'restauri_list.html', context)

def restauri_detail_view(request, slug): 
    """
    Mostra la pagina di dettaglio per un singolo progetto di restauro.
    """
    # Recupera il singolo oggetto Restauro usando lo slug dall'URL.
    # Vengono selezionati solo i restauri con 'attivo=True'.
    #
    # prefetch_related è un'ottimizzazione FONDAMENTALE:
    # Carica in anticipo tutte le fasi di lavoro e tutte le immagini collegate 
    # in sole due query aggiuntive, invece di fare una query per ogni fase e ogni immagine
    # dentro il template.
    queryset = Restauro.objects.filter(attivo=True).prefetch_related(
        'fasi_lavoro__immagini_fase'
    )
    
    restauro = get_object_or_404(queryset, slug=slug)
    
    context = {
        'restauro': restauro
    }
    
    return render(request, 'restauri_detail.html', context)