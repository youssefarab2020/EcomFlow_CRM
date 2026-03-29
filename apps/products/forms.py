from django import forms          # (1) Import du module forms
from .models import Product       # (2) Import du modèle Product

class ProductForm(forms.ModelForm):  # (3) Création d’un formulaire basé sur le modèle Product

    class Meta:
        model = Product            # (4) Lier le formulaire au modèle Product

        # (5) Champs inclus dans le formulaire (Mise à jour pour les produits)
        fields = ['name', 'sku', 'price', 'cost_price', 'stock', 'description']
        
        # (6) Personnalisation de l’affichage des champs (Design Pill-Shaped)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code produit (SKU)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix de vente ($)'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix d’achat (Coût)'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité initiale'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du produit...', 'rows': 3}),
        }