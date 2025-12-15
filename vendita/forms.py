from django import forms
from .models import RichiestaVeicolo

class RichiestaVeicoloForm(forms.ModelForm):
    class Meta:
        model = RichiestaVeicolo
        fields = ['nome', 'email', 'messaggio']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'messaggio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
        }