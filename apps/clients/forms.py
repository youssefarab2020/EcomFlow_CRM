from django import forms          # (1) Import du module forms
from .models import Client        # (2) Import du modèle Client

class ClientForm(forms.ModelForm):  # (3) Création d’un formulaire basé sur le modèle Client

    class Meta:
        model = Client             # (4) Lier le formulaire au modèle Client

        # (5) Champs inclus dans le formulaire
        fields = ['name', 'phone', 'email', 'city']
        
        # (6) Personnalisation de l’affichage des champs (Bootstrap)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom Complet'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
        }