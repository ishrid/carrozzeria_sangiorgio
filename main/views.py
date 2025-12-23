# main/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Servizio, MembroTeam, FotoOfficina, Certificazione, Partner
from restauri.models import Restauro
from vendita.models import VeicoloInVendita

 
from django.core.mail import send_mail
from .forms import ContattoForm
# View per la homepage
def home_view(request):
    
    servizi_in_evidenza = Servizio.objects.filter(attivo=True).order_by('ordine_visualizzazione')[:3] # Prendi 3 servizi attivi
    partner_home = Partner.objects.filter(in_homepage=True)
    restauri_in_evidenza = Restauro.objects.filter(attivo=True, in_evidenza=True)
    veicoli = VeicoloInVendita.objects.filter(attivo=True)
    # Qui potresti anche prendere gli ultimi restauri se hai un'app restauri
    context = {
        'servizi_in_evidenza': servizi_in_evidenza,
        'partner_home':partner_home,
        'restauri_in_evidenza':restauri_in_evidenza,
        'veicoli':veicoli
    }
    return render(request, 'index.html', context)

# View per la pagina 'Chi Siamo'
def chi_siamo_view(request):
    team_members = MembroTeam.objects.all().order_by('ordine')
    foto_list = FotoOfficina.objects.all()
    certificazioni = Certificazione.objects.all()
    context = {
        'team_members': team_members,
        'foto_list': foto_list,
        'certificazioni':certificazioni
    }
    return render(request, 'chi_siamo.html', context)





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

            send_mail(
                subject="Nuova richiesta dal sito – Carrozzeria San Giorgio",
                message=messaggio_email,
                from_email=None,  # usa DEFAULT_FROM_EMAIL
                recipient_list=["carr.sangiorgio@ticino.com"],
                reply_to=[contatto.email],
                fail_silently=False,
            )

            return redirect('main:contatti_success')
    else:
        form = ContattoForm()

    return render(request, 'contatti.html', {'form': form})


def contatti_success(request):
    return render(request, 'contatti_success.html')
  

# View per la pagina lista servizi
def servizi_list_view(request):
    servizi = Servizio.objects.filter(attivo=True).order_by('ordine_visualizzazione')
    partner = Partner.objects.all()
    context = {
        'servizi': servizi,
        'partner':partner
    }
    return render(request, 'servizi_list.html', context)

# View per la pagina dettaglio servizio
def servizi_detail_view(request, slug):
    servizio = get_object_or_404(Servizio, slug=slug, attivo=True)
    
    altri_servizi = Servizio.objects.exclude(pk=servizio.pk)
    context = {
        'servizio': servizio,
        'altri_servizi':altri_servizi,
    }
    return render(request, 'servizi_detail.html', context)

# Aggiungi qui altre view statiche se necessario (es. privacy_policy, terms_of_use)
def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')
def cookie_policy_view(request):
    return render(request, 'cookie_policy.html')



def terms_of_use_view(request):
    return render(request, 'terms_of_use.html')