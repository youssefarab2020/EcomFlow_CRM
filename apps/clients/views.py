from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError


# =========================== Partie 1: Liste des clients + Recherche
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_list(request):
    # (1) Récupérer le mot-clé de recherche depuis l'URL (?q=...)
    query = request.GET.get('q')

    # (2) Filtrer les clients appartenant uniquement à l'utilisateur connecté
    user_clients = Client.objects.filter(user=request.user)

    # (3) Appliquer la recherche si un mot-clé est fourni
    if query:
        clients = user_clients.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query)
        )
    else:
        clients = user_clients

    # (4) Envoyer les données au template
    return render(request, 'clients/client_list.html', {'clients': clients})


# =========================== Partie 2: Création d’un client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_create(request):
    # (5) Vérifier si la requête est POST (soumission du formulaire)
    if request.method == 'POST':
        form = ClientForm(request.POST)

        # (6) Validation des données du formulaire
        if form.is_valid():
            # (7) Créer l'objet sans sauvegarder immédiatement
            client = form.save(commit=False)

            # (8) Associer le client à l'utilisateur connecté
            client.user = request.user

            try:
                # (9) Sauvegarder le client en base de données
                client.save()

                # (10) Message de succès
                messages.success(request, "Super ! Le nouveau client a été ajouté avec succès.")
                return redirect('clients:list')

            except IntegrityError:
                # (11) Gestion des erreurs liées aux champs uniques (email, téléphone...)
                messages.error(request, "Impossible d'ajouter ce client : ces informations existent déjà.")

            except Exception:
                # (12) Gestion des erreurs techniques inattendues
                messages.error(request, "Erreur technique lors de la création du client.")

        else:
            # (13) Données invalides dans le formulaire
            messages.warning(request, "Veuillez vérifier les champs du formulaire.")

    else:
        # (14) Afficher un formulaire vide
        form = ClientForm()

    # (15) Retourner le formulaire au template
    return render(request, 'clients/create_client.html', {'form': form})


# =========================== Partie 3: Modification d’un client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_update(request, pk):
    # (16) Récupérer le client en vérifiant qu’il appartient à l’utilisateur
    client = get_object_or_404(Client, pk=pk, user=request.user)

    if request.method == 'POST':
        # (17) Remplir le formulaire avec les nouvelles données
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            try:
                # (18) Sauvegarder les modifications
                form.save()

                # (19) Message de succès
                messages.success(request, "Client mis à jour avec succès.")
                return redirect('clients:list')

            except IntegrityError:
                # (20) Conflit de données uniques
                messages.error(request, "Erreur : email ou téléphone déjà utilisé.")

            except Exception:
                # (21) Erreur technique
                messages.error(request, "Erreur technique lors de la modification.")
        else:
            # (22) Formulaire invalide
            messages.warning(request, "Veuillez corriger les champs invalides.")
    else:
        # (23) Charger les données existantes dans le formulaire
        form = ClientForm(instance=client)

    # (24) Retourner les données au template
    return render(request, 'clients/update_client.html', {
        'form': form,
        'client': client
    })


# =========================== Partie 4: Suppression d’un client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_delete(request, pk):
    # (25) Récupérer le client sécurisé (appartient à l'utilisateur)
    client = get_object_or_404(Client, pk=pk, user=request.user)

    # (26) Autoriser la suppression uniquement via POST (sécurité)
    if request.method == 'POST':
        try:
            # (27) Supprimer le client
            client.delete()

            # (28) Message de succès
            messages.success(request, "Client supprimé avec succès.")

        except Exception:
            # (29) Erreur si le client est lié à d'autres données (ex: ventes)
            messages.error(request, "Impossible de supprimer ce client lié à des données existantes.")

        return redirect('clients:list')

    # (30) Redirection si accès direct (GET)
    return redirect('clients:list')