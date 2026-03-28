from django.contrib import admin  # (1) Import du module admin de Django
from .models import Client       # (2) Import du modèle Client

@admin.register(Client)          # (3) Enregistrer le modèle Client dans l’admin
class ClientAdmin(admin.ModelAdmin):

    # (4) Les champs affichés dans la liste des clients
    list_display = ('name', 'phone', 'email', 'city', 'created_at')

    # (5) Filtres disponibles à droite (par ville)
    list_filter = ('city',)

    # (6) Barre de recherche (nom, téléphone, email)
    search_fields = ('name', 'phone', 'email')