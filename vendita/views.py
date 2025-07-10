from django.shortcuts import render, get_object_or_404
from .models import VeicoloInVendita

def veicoli_list_view(request):
    """
    Visualizza la lista di tutti i veicoli in vendita attivi.
    Include logica di filtro/ordinamento.
    """
    veicoli = VeicoloInVendita.objects.filter(attivo=True)

    # Implementa qui la logica di filtro/ordinamento se necessaria
    # Esempio: filtro per marca
    marca_filter = request.GET.get('marca', None)
    if marca_filter:
        veicoli = veicoli.filter(marca__iexact=marca_filter)

    # Esempio: ordinamento per prezzo
    order_by = request.GET.get('order_by', '-data_pubblicazione')
    veicoli = veicoli.order_by(order_by)

    # Passa i filtri disponibili al template (es. elenco marche uniche)
    marche_disponibili = VeicoloInVendita.objects.filter(attivo=True).values_list('marca', flat=True).distinct()

    context = {
        'veicoli': veicoli,
        'marche_disponibili': sorted(list(marche_disponibili)),
        'selected_marca': marca_filter,
        'selected_order_by': order_by,
    }
    return render(request, 'veicoli_list.html', context)

def veicoli_detail_view(request, slug):
    """
    Visualizza i dettagli di un singolo veicolo in vendita.
    """
    veicolo = get_object_or_404(VeicoloInVendita, slug=slug, attivo=True)
    # Recupera altri 3 veicoli disponibili per la sezione "Potrebbe interessarti"
    altri_veicoli = VeicoloInVendita.objects.filter(attivo=True, status='disponibile').exclude(pk=veicolo.pk)[:3]
    
    # Potresti passare anche un form per il contatto diretto per questo veicolo
    # from main.forms import ContattoForm # Se crei un form in main app
    # contact_form = ContattoForm(initial={'messaggio': f'Richiesta informazioni per {veicolo.marca} {veicolo.modello} ({veicolo.anno})'})
    dotazione_list = []
    if veicolo.dotazione_opzionale:
        # Divide la stringa per virgola o per newline
        dotazione_list = [item.strip() for item in veicolo.dotazione_opzionale.replace('\n', ',').split(',') if item.strip()]

    context = {
        'veicolo': veicolo,
        'altri_veicoli': altri_veicoli,
        'dotazione_list': dotazione_list,
    }
    
    return render(request, 'veicoli_detail.html', context)

 
 
     