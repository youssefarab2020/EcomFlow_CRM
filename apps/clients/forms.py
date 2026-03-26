# apps/clients/forms.py
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'city']
        
        # إضافة "Bootstrap Classes" باش يجي الديكور نقي
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom Complet'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
        }