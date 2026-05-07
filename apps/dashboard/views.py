from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required

# (1) Importation des modèles métiers
from apps.ventes.models import Vente
from apps.clients.models import Client
from apps.products.models import Product


# =========================== Dashboard Principal
@login_required(login_url='/login/')
def dashboard_home(request):
    # (2) Récupérer l'utilisateur actuellement connecté
    current_user = request.user

    # (3) Calcul du chiffre d'affaires total (revenus)
    # Filtré uniquement par utilisateur (isolation des données SaaS)
    total_revenus = Vente.objects.filter(user=current_user).aggregate(
        total=Sum('total_amount')
    )['total'] or 0.00

    # (4) Nombre total de ventes
    total_ventes = Vente.objects.filter(user=current_user).count()

    # (5) Nombre total de clients
    total_clients = Client.objects.filter(user=current_user).count()

    # (6) Produits avec stock faible (seuil ≤ 5)
    produits_faible_stock = Product.objects.filter(
        user=current_user,
        stock__lte=5
    )

    # (7) Top 5 produits les plus vendus
    # Annotation pour compter le nombre de ventes par produit
    top_produits = Product.objects.filter(user=current_user).annotate(
        nombre_ventes=Count('ventes')
    ).order_by('-nombre_ventes')[:5]

    # (8) Regroupement des données pour le template
    context = {
        'total_revenus': total_revenus,
        'total_ventes': total_ventes,
        'total_clients': total_clients,
        'produits_faible_stock': produits_faible_stock,
        'top_produits': top_produits,
    }

    # (9) Rendu de la vue dashboard
    return render(request, 'dashboard/index.html', context)