from django.shortcuts import render, redirect, get_object_or_404
from .forms import VenteForm
from .models import Vente
from django.db.models import Q
from django.contrib.auth.decorators import login_required # (NOUVEAU) Pour la sécurité

# =========================== Partie 1: Affichage & Recherche
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_list(request):
    query = request.GET.get('q')

    # On filtre pour n'afficher que les ventes de l'utilisateur connecté
    user_ventes = Vente.objects.filter(user=request.user)

    if query:
        # Recherche parmi les ventes de l'utilisateur (Client ou Produit)
        ventes = user_ventes.filter(
            Q(client__name__icontains=query) | 
            Q(product__name__icontains=query)
        )
    else:
        ventes = user_ventes

    return render(request, 'ventes/vente_list.html', {'ventes': ventes})

# =========================== Partie 2: Enregistrement d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_create(request):
    if request.method == 'POST':
        # (MODIFIÉ) On passe le user au formulaire pour filtrer les listes
        form = VenteForm(request.POST, user=request.user) 
        
        if form.is_valid():
            vente = form.save(commit=False)
            # (IMPORTANT) On lie la vente à l'utilisateur actuel
            vente.user = request.user
            vente.save() 
            return redirect('ventes:list')
    else:
        # (MODIFIÉ) On passe le user au formulaire vide (GET)
        form = VenteForm(user=request.user)

    return render(request, 'ventes/vente_create.html', {'form': form})

# =========================== Partie 3: Modification d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_update(request, pk):
    # Sécurité : On vérifie que la vente appartient bien à l'utilisateur
    vente = get_object_or_404(Vente, pk=pk, user=request.user)
    
    ancienne_qte = vente.quantity 

    if request.method == 'POST':
        # (MODIFIÉ) On passe le user au formulaire pour filtrer les listes
        form = VenteForm(request.POST, instance=vente, user=request.user)
        
        if form.is_valid():
            nouvelle_qte = form.cleaned_data['quantity']
            
            try:
                # Logique de stock conservée
                vente.update_quantite(nouvelle_qte, ancienne_qte)
                
                # On s'assure que le user reste le même lors du save
                vente_modifiee = form.save(commit=False)
                vente_modifiee.user = request.user
                vente_modifiee.save()
                
                return redirect('ventes:list')
                
            except ValueError as e:
                form.add_error('quantity', str(e))
    else:
        # (MODIFIÉ) On passe le user au formulaire de modification (GET)
        form = VenteForm(instance=vente, user=request.user)

    return render(request, 'ventes/vente_update.html', {'form': form, 'vente': vente})

# =========================== Partie 4: Suppression d'une Vente
@login_required(login_url='accounts:login', redirect_field_name=None)
def vente_delete(request, pk):
    # Sécurité : On vérifie que la vente appartient bien à l'utilisateur
    vente = get_object_or_404(Vente, pk=pk, user=request.user)

    if request.method == 'POST':
        # Optionnel : Remettre les produits en stock avant suppression si nécessaire
        vente.delete()
        return redirect('ventes:list')

    return redirect('ventes:list')