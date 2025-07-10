from django.urls import path
from . import views

app_name = 'restauri' # Definisci un namespace per questa app

urlpatterns = [
    path('', views.restauri_list_view, name='lista_restauri'),
    path('<slug:slug>/', views.restauri_detail_view, name='dettaglio_restauro'),
]