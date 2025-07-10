from django.urls import path
from . import views

app_name = 'vendita' # Definisci un namespace per questa app

urlpatterns = [
    path('', views.veicoli_list_view, name='lista_veicoli'),
    path('<slug:slug>/', views.veicoli_detail_view, name='dettaglio_veicolo'),
]