from django import forms
from .models import Vente

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        
        # (1) Champs que l'utilisateur doit remplir uniquement
        # total_amount est exclu car editable=False
        # Le champ 'user' n'est pas inclus ici pour des raisons de sécurité
        fields = ['client', 'product', 'quantity', 'price']

        # (2) Personnalisation de l'apparence avec Bootstrap
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-select shadow-sm', 
                'placeholder': 'Sélectionner le client'
            }),
            'product': forms.Select(attrs={
                'class': 'form-select shadow-sm', 
                'placeholder': 'Sélectionner le produit'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'min': '1',
                'placeholder': 'Quantité'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'placeholder': 'Prix unitaire (laisser vide pour prix par défaut)'
            }),
        }

        # (3) Étiquettes des champs en français
        labels = {
            'client': 'Client',
            'product': 'Produit',
            'quantity': 'Quantité vendue',
            'price': 'Prix de vente (DH)',
        }

    # =========================================================================
    # AJOUT IMPORTANT : Filtrage des listes déroulantes (Client et Produit)
    # =========================================================================
    def __init__(self, *args, **kwargs):
        # Récupérer l'utilisateur passé depuis la vue (views.py)
        user = kwargs.pop('user', None)
        super(VenteForm, self).__init__(*args, **kwargs)
        
        if user:
            # On filtre pour n'afficher que les clients et produits de l'utilisateur connecté
            # Cela évite d'importer les modèles Client et Product et prévient les erreurs d'importation circulaire
            self.fields['client'].queryset = self.fields['client'].queryset.filter(user=user)
            self.fields['product'].queryset = self.fields['product'].queryset.filter(user=user)

    # (4) Validation personnalisée pour vérifier le stock avant la vente
    def clean_quantity(self):
        # (1) Récupérer les données saisies
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        
        if product:
            # (2) Vérifier si le produit est en rupture de stock totale
            if product.stock <= 0:
                raise forms.ValidationError(
                    f"Rupture de stock ! Le produit '{product.name}' n'est plus disponible."
                )

            # (3) Vérifier si la quantité demandée dépasse le stock actuel
            if quantity > product.stock:
                raise forms.ValidationError(
                    f"Stock insuffisant ! Il ne reste que {product.stock} unités."
                )

            # (4) Protection : Empêcher la saisie d'une quantité nulle ou négative
            if quantity <= 0:
                raise forms.ValidationError(
                    "La quantité de vente doit être supérieure à zéro."
                )

        # (5) Retourner la valeur validée
        return quantity