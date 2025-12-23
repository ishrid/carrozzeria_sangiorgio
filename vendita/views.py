import os
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import VeicoloInVendita
from .forms import RichiestaVeicoloForm

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
    veicolo = get_object_or_404(VeicoloInVendita, slug=slug, attivo=True)

    altri_veicoli = (
        VeicoloInVendita.objects
        .filter(attivo=True, status='disponibile')
        .exclude(pk=veicolo.pk)[:3]
    )

    dotazione_list = []
    if veicolo.dotazione_opzionale:
        dotazione_list = [
            item.strip()
            for item in veicolo.dotazione_opzionale.replace('\n', ',').split(',')
            if item.strip()
        ]

    if request.method == 'POST':
        form = RichiestaVeicoloForm(request.POST)
        if form.is_valid():
            richiesta = form.save(commit=False)
            richiesta.veicolo = veicolo
            richiesta.save()

            # -------------------------
            # INVIO EMAIL CON SENDGRID
            # -------------------------
            SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

            messaggio_email = f"""
Nuova richiesta veicolo dal sito Carrozzeria San Giorgio

VEICOLO:
{veicolo.marca} {veicolo.modello}
Anno: {veicolo.anno}
Km: {veicolo.chilometraggio}

CLIENTE:
Nome: {richiesta.nome}
Email: {richiesta.email}

MESSAGGIO:
{richiesta.messaggio}
"""

            if SENDGRID_API_KEY:
                payload = {
                    "personalizations": [{
                        "to": [{"email": "carr.sangiorgio@ticino.com"}],
                        "subject": f"[VEICOLO] {veicolo.marca} {veicolo.modello} – {richiesta.nome}",
                        "reply_to": {"email": richiesta.email},
                    }],
                    "from": {"email": "csg.agno@gmail.com"},
                    "content": [{
                        "type": "text/plain",
                        "value": messaggio_email
                    }]
                }

                headers = {
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    json=payload,
                    headers=headers,
                    timeout=10
                )

                if response.status_code != 202:
                    print("❌ ERRORE SENDGRID (VEICOLO):", response.status_code, response.text)
            else:
                print("❌ SENDGRID_API_KEY non trovata")

            messages.success(request, "Richiesta inviata con successo!")
            return redirect(request.path)
    else:
        form = RichiestaVeicoloForm(initial={
            'messaggio': (
                f"Sono interessato al veicolo {veicolo.marca} {veicolo.modello} "
                f"(Anno {veicolo.anno}, Km {veicolo.chilometraggio})."
            )
        })

    context = {
        'veicolo': veicolo,
        'altri_veicoli': altri_veicoli,
        'dotazione_list': dotazione_list,
        'form': form
    }

    return render(request, 'veicoli_detail.html', context)
 


 
 