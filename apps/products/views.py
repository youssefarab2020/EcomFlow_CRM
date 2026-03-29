from django.shortcuts import render, redirect, get_object_or_404  # (1) Fonctions utiles pour les views
from .forms import ProductForm                                   # (2) Import du formulaire Product
from .models import Product                                     # (3) Import du modèle Product
from django.db.models import Q                                   # (4) Pour faire des recherches avancées

# =========================== Partie 1: Liste des Produits + Recherche
def product_list(request):
    # (5) Récupérer la valeur de recherche (input name="q")
    query = request.GET.get('q')
    
    if query:
        # (6) Filtrer les produits par nom ou SKU
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query)
        )
    else:
        # (7) Afficher tous les produits (le tri est géré par Meta dans models.py)
        products = Product.objects.all()

    # (8) Envoyer les données au template
    return render(request, 'products/product_list.html', {'products': products})

# ===================================== Partie 2: Création de Produit
def product_create(request):

    if request.method == 'POST':          # (1) Vérifier si le formulaire est envoyé
        form = ProductForm(request.POST)   # (2) Remplir le formulaire avec les données

        if form.is_valid():               # (3) Vérifier si les données sont valides
            form.save()                   # (4) Enregistrer dans la base de données
            return redirect('products:product_list')  # (5) Redirection vers la liste

    else:
        form = ProductForm()               # (6) Formulaire vide (GET)

    return render(request, 'products/product_create.html', {'form': form})  # (7) Affichage

# ==================================== Partie 3: Modification de Produit
def product_update(request, pk):

    product = get_object_or_404(Product, pk=pk)  # (1) Récupérer le produit ou erreur 404

    if request.method == 'POST':
        # (2) Charger les données + instance pour modification
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()                       # (3) Sauvegarder les modifications
            return redirect('products:product_list')   # (4) Redirection

    else:
        form = ProductForm(instance=product)    # (5) Remplir avec anciennes données

    return render(request, 'products/product_update.html', {
        'form': form,
        'product': product
    })  # (6) Envoyer au template

# ==================== Partie 4: Suppression de Produit
def product_delete(request, pk):

    product = get_object_or_404(Product, pk=pk)  # (1) Récupérer le produit

    if request.method == 'POST':               # (2) Vérifier POST 
        product.delete()                        # (3) Supprimer
        return redirect('products:product_list')        # (4) Retour à la liste

    return redirect('products:product_list')            # (5) Sécurité: empêcher la suppression via GET