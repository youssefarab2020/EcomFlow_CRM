from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # (1) Gestion des messages utilisateur
from django.db import IntegrityError  # (2) Gestion des erreurs liées à la base de données


# =========================== Partie 1: Liste des produits + Recherche
@login_required(login_url='accounts:login', redirect_field_name=None)
def product_list(request):
    # (3) Récupérer le mot-clé de recherche depuis l'URL
    query = request.GET.get('q')

    # (4) Filtrer les produits appartenant à l'utilisateur connecté
    user_products = Product.objects.filter(user=request.user)

    # (5) Appliquer la recherche si un mot-clé est fourni
    if query:
        products = user_products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )
    else:
        products = user_products

    # (6) Envoyer les produits au template
    return render(request, 'products/product_list.html', {'products': products})


# ===================================== Partie 2: Création de produit
@login_required(login_url='accounts:login', redirect_field_name=None)
def product_create(request):
    # (7) Vérifier si la requête est POST
    if request.method == 'POST':
        form = ProductForm(request.POST)

        # (8) Validation du formulaire
        if form.is_valid():
            # (9) Création de l'objet sans sauvegarde immédiate
            product = form.save(commit=False)

            # (10) Associer le produit à l'utilisateur connecté
            product.user = request.user

            try:
                # (11) Sauvegarde en base de données
                product.save()

                # (12) Message de succès
                messages.success(request, "Produit ajouté avec succès.")
                return redirect('products:product_list')

            except IntegrityError:
                # (13) Gestion des conflits de données (ex: SKU unique)
                messages.error(request, "Erreur : Ce SKU est déjà utilisé.")

            except Exception:
                # (14) Gestion des erreurs techniques
                messages.error(request, "Erreur technique lors de la création.")
        else:
            # (15) Formulaire invalide
            messages.warning(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        # (16) Initialiser un formulaire vide
        form = ProductForm()

    # (17) Retourner le formulaire au template
    return render(request, 'products/product_create.html', {'form': form})


# ==================================== Partie 3: Modification de produit
@login_required(login_url='accounts:login', redirect_field_name=None)
def product_update(request, pk):
    # (18) Récupérer le produit sécurisé (lié à l'utilisateur)
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        # (19) Charger les données modifiées dans le formulaire
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            try:
                # (20) Sauvegarder les modifications
                form.save()

                # (21) Message de succès
                messages.success(request, "Produit mis à jour avec succès.")
                return redirect('products:product_list')

            except IntegrityError:
                # (22) Conflit sur champ unique (SKU)
                messages.error(request, "Erreur : Ce SKU est déjà utilisé.")

            except Exception:
                # (23) Erreur technique
                messages.error(request, "Erreur technique lors de la modification.")
        else:
            # (24) Formulaire invalide
            messages.warning(request, "Veuillez corriger les champs invalides.")
    else:
        # (25) Charger les données existantes dans le formulaire
        form = ProductForm(instance=product)

    # (26) Retourner les données au template
    return render(request, 'products/product_update.html', {
        'form': form,
        'product': product
    })


# ==================== Partie 4: Suppression de produit
@login_required(login_url='accounts:login', redirect_field_name=None)
def product_delete(request, pk):
    # (27) Récupérer le produit sécurisé
    product = get_object_or_404(Product, pk=pk, user=request.user)

    # (28) Autoriser la suppression uniquement via POST (sécurité)
    if request.method == 'POST':
        try:
            # (29) Supprimer le produit
            product.delete()

            # (30) Message de succès
            messages.success(request, "Produit supprimé avec succès.")

        except Exception:
            # (31) Erreur si le produit est مرتبط ببيانات أخرى (ex: ventes)
            messages.error(request, "Impossible de supprimer ce produit. Il est peut-être lié à des ventes.")

        return redirect('products:product_list')

    # (32) Redirection si accès direct en GET
    return redirect('products:product_list')