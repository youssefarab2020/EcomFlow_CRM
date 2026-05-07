from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.contrib import messages  # (1) Gestion des messages utilisateur
from django.contrib.auth.decorators import login_required  # (2) Protection des vues

from .forms import VenteForm
from .models import Vente


# =========================== Partie 1: Affichage & Recherche
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_list(request):
    # (3) Récupérer le mot-clé de recherche
    query = request.GET.get('q')

    # (4) Filtrer les ventes de l'utilisateur connecté uniquement
    user_ventes = Vente.objects.filter(user=request.user)

    # (5) Appliquer la recherche si un mot-clé existe
    if query:
        ventes = user_ventes.filter(
            Q(client__name__icontains=query) |
            Q(product__name__icontains=query)
        )
    else:
        ventes = user_ventes

    # (6) Envoyer les données au template
    return render(request, 'ventes/vente_list.html', {'ventes': ventes})


# =========================== Partie 2: Enregistrement d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_create(request):
    # (7) Vérifier si la requête est POST
    if request.method == 'POST':
        # (8) Initialiser le formulaire avec l'utilisateur (filtrage sécurisé)
        form = VenteForm(request.POST, user=request.user)

        # (9) Validation du formulaire
        if form.is_valid():
            # (10) Création de l'objet sans sauvegarde immédiate
            vente = form.save(commit=False)

            # (11) Associer la vente à l'utilisateur connecté
            vente.user = request.user

            try:
                # (12) Sauvegarde en base de données
                vente.save()

                # (13) Message de succès
                messages.success(request, "Vente enregistrée avec succès.")
                return redirect('ventes:list')

            except IntegrityError:
                # (14) Erreur liée aux relations (client/produit)
                messages.error(request, "Erreur : Le client ou le produit sélectionné est invalide.")

            except Exception:
                # (15) Erreur technique générale
                messages.error(request, "Erreur technique lors de l'enregistrement de la vente.")
        else:
            # (16) Formulaire invalide
            messages.warning(request, "Veuillez corriger les champs invalides.")
    else:
        # (17) Initialiser un formulaire vide
        form = VenteForm(user=request.user)

    # (18) Retourner le formulaire au template
    return render(request, 'ventes/vente_create.html', {'form': form})


# =========================== Partie 3: Modification d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_update(request, pk):
    # (19) Récupérer la vente sécurisée
    vente = get_object_or_404(Vente, pk=pk, user=request.user)

    # (20) Sauvegarder l'ancienne quantité pour gérer le stock
    ancienne_qte = vente.quantity

    if request.method == 'POST':
        # (21) Charger les données modifiées
        form = VenteForm(request.POST, instance=vente, user=request.user)

        if form.is_valid():
            # (22) Nouvelle quantité demandée
            nouvelle_qte = form.cleaned_data['quantity']

            try:
                # (23) Transaction atomique pour garantir la cohérence des données
                with transaction.atomic():
                    # (24) Mise à jour du stock via méthode métier
                    vente.update_quantite(nouvelle_qte, ancienne_qte)

                    # (25) Sauvegarde de la vente modifiée
                    vente_modifiee = form.save(commit=False)
                    vente_modifiee.user = request.user
                    vente_modifiee.save()

                # (26) Message de succès
                messages.success(request, "Vente modifiée avec succès.")
                return redirect('ventes:list')

            except ValueError as e:
                # (27) Erreur métier (ex: stock insuffisant)
                form.add_error('quantity', str(e))
                messages.error(request, str(e))

            except Exception:
                # (28) Erreur technique
                messages.error(request, "Erreur technique lors de la modification.")
        else:
            # (29) Formulaire invalide
            messages.warning(request, "Veuillez corriger les champs invalides.")
    else:
        # (30) Charger les données existantes
        form = VenteForm(instance=vente, user=request.user)

    # (31) Retourner les données au template
    return render(request, 'ventes/vente_update.html', {'form': form, 'vente': vente})


# =========================== Partie 4: Suppression d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_delete(request, pk):
    # (32) Récupérer la vente sécurisée
    vente = get_object_or_404(Vente, pk=pk, user=request.user)

    # (33) Autoriser la suppression uniquement via POST
    if request.method == 'POST':
        try:
            # (34) Transaction pour garantir cohérence stock + suppression
            with transaction.atomic():
                # (35) Restaurer le stock du produit lié
                produit = vente.product
                produit.stock += vente.quantity
                produit.save()

                # (36) Supprimer la vente
                vente.delete()

            # (37) Message de succès
            messages.success(request, "Vente supprimée et stock restauré.")

        except Exception:
            # (38) Erreur technique
            messages.error(request, "Erreur technique lors de la suppression.")

        return redirect('ventes:list')

    # (39) Redirection si accès non autorisé
    return redirect('ventes:list')