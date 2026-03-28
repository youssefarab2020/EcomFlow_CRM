from django.shortcuts import render, redirect, get_object_or_404  # (1) Fonctions utiles pour les views
from .forms import ClientForm                                      # (2) Import du formulaire
from .models import Client                                         # (3) Import du modèle Client
from django.db.models import Q                                     # (4) Pour faire des recherches avancées
#===========================Partie 1: Imports + Search View
def client_list(request):
    # (5) Récupérer la valeur de recherche (input name="q")
    query = request.GET.get('q')
    
    if query:
        # (6) Filtrer les clients par nom, téléphone ou ville
        clients = Client.objects.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) |
            Q(city__icontains=query)
        )
    else:
        # (7) Afficher tous les clients si pas de recherche
        clients = Client.objects.all()

    # (8) Envoyer les données au template
    return render(request, 'clients/client_list.html', {'clients': clients})

#=====================================Partie 2: Create View
def client_create(request):

    if request.method == 'POST':          # (1) Vérifier si le formulaire est envoyé
        form = ClientForm(request.POST)   # (2) Remplir le formulaire avec les données

        if form.is_valid():               # (3) Vérifier si les données sont valides
            form.save()                   # (4) Enregistrer dans la base de données
            return redirect('clients:list')  # (5) Redirection vers la liste

    else:
        form = ClientForm()               # (6) Formulaire vide (GET)

    return render(request, 'clients/create_client.html', {'form': form})  # (7) Affichage

#====================================Partie 3: Update View===============================================

def client_update(request, pk):

    client = get_object_or_404(Client, pk=pk)  # (1) Récupérer le client ou erreur 404

    if request.method == 'POST':
        # (2) Charger les données + instance pour modification
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()                       # (3) Sauvegarder les modifications
            return redirect('clients:list')   # (4) Redirection

    else:
        form = ClientForm(instance=client)    # (5) Remplir avec anciennes données

    return render(request, 'clients/update_client.html', {
        'form': form,
        'client': client
    })  # (6) Envoyer au template

#====================Partie 4: Delete View
def client_delete(request, pk):

    client = get_object_or_404(Client, pk=pk)  # (1) Récupérer le client

    if request.method == 'POST':               # (2) Vérifier POST 
        client.delete()                        # (3) Supprimer
        return redirect('clients:list')        # (4) Retour à la liste

    return redirect('clients:list')            # (5) Empêcher la suppression via une requête GET