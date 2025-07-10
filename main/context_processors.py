from .models import Servizio

def servizi_navbar(request):
    """
    Rende la lista dei servizi attivi disponibile a tutti i template per la navbar.
    """
    active_servizi = Servizio.objects.filter(attivo=True).order_by('ordine_visualizzazione')
    return {'servizi_menu': active_servizi}