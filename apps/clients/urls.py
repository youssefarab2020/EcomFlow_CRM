from django.urls import path   # (1) Import de path pour définir les routes
from . import views            # (2) Import des views de l’application

app_name = 'clients'           # (3) Nom de l’application pour namespacing

urlpatterns = [
    # (4) Liste des URLs de l’application

    path('', views.client_list, name='list'),              # (5) Afficher la liste des clients
    path('add/', views.client_create, name='create'),      # (6) Ajouter un nouveau client
    path('<int:pk>/update/', views.client_update, name='update'),  # (7) Modifier un client
    path('<int:pk>/delete/', views.client_delete, name='delete'),  # (8) Supprimer un client
]