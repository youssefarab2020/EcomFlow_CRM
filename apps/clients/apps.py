from django.apps import AppConfig   # (1) Import de AppConfig pour configurer l'application

class ClientsConfig(AppConfig):     # (2) Configuration de l’application "clients"
    
    # (3) Type par défaut pour les clés primaires (id auto-incrémenté)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # (4) Nom complet de l’application (chemin Python)
    name = 'apps.clients'