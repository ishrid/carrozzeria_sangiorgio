# main/views.py
import os
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Servizio, MembroTeam, FotoOfficina, Certificazione, Partner
from .forms import ContattoForm

from restauri.models import Restauro
from vendita.models import VeicoloInVendita


# -------------------------
# HOMEPAGE
# -------------------------
def home_view(request):
    servizi_in_evidenza = Servizio.objects.filter(attivo=True).order_by('ordine_visualizzazione')[:3]
    partner_home = Partner.objects.filter(in_homepage=True)
    restauri_in_evidenza = Restauro.objects.filter(attivo=True, in_evidenza=True)
    veicoli = VeicoloInVendita.objects.filter(attivo=True)

    context = {
        'servizi_in_evidenza': servizi_in_evidenza,
        'partner_home': partner_home,
        'restauri_in_evidenza': restauri_in_evidenza,
        'veicoli': veicoli,
    }
    return render(request, 'index.html', context)


# -------------------------
# CHI SIAMO
# -------------------------
def chi_siamo_view(request):
    team_members = MembroTeam.objects.all().order_by('ordine')
    foto_list = FotoOfficina.objects.all()
    certificazioni = Certificazione.objects.all()

    context = {
        'team_members': team_members,
        'foto_list': foto_list,
        'certificazioni': certificazioni,
    }
    return render(request, 'chi_siamo.html', context)


# -------------------------
# CONTATTI (SENDGRID API)
# -------------------------
def contatti_view(request):
    if request.method == 'POST':
        form = ContattoForm(request.POST)
        if form.is_valid():
            contatto = form.save()

            messaggio_email = f"""
Nuova richiesta dal sito Carrozzeria San Giorgio

Nome: {contatto.nome}
Email: {contatto.email}
Telefono: {contatto.telefono}
Tipo richiesta: {contatto.tipo_richiesta}

Messaggio:
{contatto.messaggio}
"""

            SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

            if SENDGRID_API_KEY:
                url = "https://api.sendgrid.com/v3/mail/send"

                payload = {
                    "personalizations": [
                        {
                            "to": [{"email": "csg.agno@gmail.com"}],
                            "subject": f"Richiesta {contatto.tipo_richiesta} – {contatto.nome}",
                        }
                    ],
                    "from": {"email": "csg.agno@gmail.com"},
                    "reply_to": {"email": contatto.email},
                    "content": [
                        {
                            "type": "text/plain",
                            "value": messaggio_email
                        }
                    ]
                }

                headers = {
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )

                if response.status_code != 202:
                    print("❌ ERRORE SENDGRID:", response.status_code, response.text)
            else:
                print("❌ SENDGRID_API_KEY non trovata")

            return redirect('main:contatti_success')
    else:
        form = ContattoForm()

    return render(request, 'contatti.html', {'form': form})


def contatti_success(request):
    return render(request, 'contatti_success.html')


# -------------------------
# SERVIZI
# -------------------------
def servizi_list_view(request):
    servizi = Servizio.objects.filter(attivo=True).order_by('ordine_visualizzazione')
    partner = Partner.objects.all()

    context = {
        'servizi': servizi,
        'partner': partner,
    }
    return render(request, 'servizi_list.html', context)


def servizi_detail_view(request, slug):
    servizio = get_object_or_404(Servizio, slug=slug, attivo=True)
    altri_servizi = Servizio.objects.exclude(pk=servizio.pk)

    context = {
        'servizio': servizio,
        'altri_servizi': altri_servizi,
    }
    return render(request, 'servizi_detail.html', context)


# -------------------------
# PAGINE STATICHE
# -------------------------
def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


def cookie_policy_view(request):
    return render(request, 'cookie_policy.html')


def terms_of_use_view(request):
    return render(request, 'terms_of_use.html')


# -------------------------
# TEST SENDGRID (DEBUG)
# -------------------------
def test_email(request):
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

    if not SENDGRID_API_KEY:
        return HttpResponse("❌ SENDGRID_API_KEY non trovata", status=500)

    url = "https://api.sendgrid.com/v3/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [{"email": "csg.agno@gmail.com"}],
                "subject": "Test email SendGrid API"
            }
        ],
        "from": {"email": "csg.agno@gmail.com"},
        "content": [
            {
                "type": "text/plain",
                "value": "Email inviata correttamente tramite SendGrid API 🚀"
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code == 202:
        return HttpResponse("✅ Email inviata correttamente (SendGrid API)")
    else:
        return HttpResponse(
            f"❌ Errore SendGrid API: {response.status_code}<br>{response.text}",
            status=500
        )
