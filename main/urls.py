# main/urls.py
from django.urls import path
from . import views

app_name = 'main' # Definisci un namespace per questa app

urlpatterns = [
    path('', views.home_view, name='home'),
    path('chi-siamo/', views.chi_siamo_view, name='chi_siamo'),
    path('contatti/', views.contatti_view, name='contatti'),
    path('servizi/', views.servizi_list_view, name='servizi_list'),
    path('servizi/<slug:slug>/', views.servizi_detail_view, name='servizi_detail'),
    path('privacy/', views.privacy_policy_view, name='privacy_policy'),
    path('termini-di-uso/', views.terms_of_use_view, name='terms_of_use'),
]