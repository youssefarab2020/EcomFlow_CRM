from django.urls import path   # (1) Import de path pour définir les routes
from . import views            # (2) Import des views de l’application

app_name = 'products'          # (3) Nom de l’application pour namespacing (Important!)

urlpatterns = [
    # (4) Liste des URLs de l’application Products

    path('', views.product_list, name='product_list'),              # (5) Afficher le catalogue des produits
    path('add/', views.product_create, name='product_create'),      # (6) Ajouter un nouveau produit
    path('<int:pk>/update/', views.product_update, name='product_update'), # (7) Modifier un produit
    path('<int:pk>/delete/', views.product_delete, name='product_delete'), # (8) Supprimer un produit
]