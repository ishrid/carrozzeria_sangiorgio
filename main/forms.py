from django import forms
from .models import Contatto

class ContattoForm(forms.ModelForm):
    class Meta:
        model = Contatto
        fields = ['nome', 'email', 'telefono', 'tipo_richiesta', 'messaggio']
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'telefono': 'Telefono',
            'tipo_richiesta': 'Tipo di richiesta',
            'messaggio': 'Come possiamo aiutarti?',
        }
        widgets = {
    'nome': forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Il tuo nome'
    }),
    'email': forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Indirizzo email'
    }),
    'telefono': forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Numero di telefono (opzionale)'
    }),
    'tipo_richiesta': forms.Select(attrs={
        'class': 'form-select form-select-lg'
    }),
    'messaggio': forms.Textarea(attrs={
        'class': 'form-control form-control-lg',
        'rows': 5,
        'placeholder': 'Scrivi qui il tuo messaggio...'
    }),
}
