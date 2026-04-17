from django.urls import path   # (1) Import de path pour définir les routes
from . import views            # (2) Import des views de l’application Ventes

app_name = 'ventes'            # (3) Nom de l’application pour namespacing (utilisé dans {% url 'ventes:...' %})

urlpatterns = [
    # (4) Liste des URLs de l'application Ventes

    # (5) Journal des ventes (Liste + Recherche)
    path('', views.vente_list, name='list'),

    # (6) Enregistrer une nouvelle transaction (Add)
    path('nouveau/', views.vente_create, name='create'),

    # (7) Modifier une vente existante (Update)
    path('<int:pk>/modifier/', views.vente_update, name='update'),

    # (8) Supprimer une vente (Delete)
    path('<int:pk>/supprimer/', views.vente_delete, name='delete'),
]