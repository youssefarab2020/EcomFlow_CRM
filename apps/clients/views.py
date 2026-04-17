from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client
from django.db.models import Q
from django.contrib.auth.decorators import login_required  # (NOUVEAU) Pour protéger les vues

#=========================== Partie 1: Liste des Clients + Recherche
@login_required(login_url='accounts:login', redirect_field_name=None)  # Redirige vers login si non connecté
def client_list(request):
    query = request.GET.get('q')
    
    # On commence toujours par filtrer par l'utilisateur connecté
    user_clients = Client.objects.filter(user=request.user)
    
    if query:
        # On filtre la recherche PARMI les clients de l'utilisateur uniquement
        clients = user_clients.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) |
            Q(city__icontains=query)
        )
    else:
        clients = user_clients

    return render(request, 'clients/client_list.html', {'clients': clients})

#===================================== Partie 2: Créer un Client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # (MODIFIÉ) On ne sauvegarde pas tout de suite en BDD
            client = form.save(commit=False)
            # On lie le client à l'utilisateur actuel
            client.user = request.user
            # On sauvegarde réellement
            client.save()
            return redirect('clients:list')
    else:
        form = ClientForm()

    return render(request, 'clients/create_client.html', {'form': form})

#==================================== Partie 3: Modifier un Client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_update(request, pk):
    # (MODIFIÉ) get_object_or_404 vérifie maintenant le PK ET si le client appartient à l'utilisateur
    # Si un utilisateur tente de modifier le client d'un autre via l'URL, il aura une erreur 404.
    client = get_object_or_404(Client, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/update_client.html', {
        'form': form,
        'client': client
    })

#==================== Partie 4: Supprimer un Client
@login_required(login_url='accounts:login', redirect_field_name=None)
def client_delete(request, pk):
    # Sécurité : on vérifie que le client appartient bien à l'utilisateur
    client = get_object_or_404(Client, pk=pk, user=request.user)

    if request.method == 'POST':
        client.delete()
        return redirect('clients:list')

    return redirect('clients:list')