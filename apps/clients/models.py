from django.db import models  # (1) Import du module models
from django.conf import settings



class Client(models.Model):
    # (2) Nom du client
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    # (3) Numéro de téléphone (avec exemple affiché)
    phone = models.CharField(max_length=20, help_text="Example: +212600000000")

    # (4) Email unique (optionnel)
    email = models.EmailField( blank=True, null=True)

    # (5) Ville (optionnelle)
    city = models.CharField(max_length=100, blank=True)

    # (6) Date de création automatique
    created_at = models.DateTimeField(auto_now_add=True)

    # (7) Représentation du client dans l’admin
    def __str__(self):
        return self.name

    # (8) Configuration du modèle
    class Meta:
        ordering = ['-created_at']  # Trier du plus récent au plus ancien
        constraints = [
            models.UniqueConstraint(fields=['user', 'email'], name='unique_client_email_per_user')
        ]
    @property
    def marketing_status(self):
        """
        (1) Déterminer la stratégie marketing selon le nombre de commandes :
            - 0 commandes → Objectif : convertir en premier achat
            - 1 commande  → Objectif : réassurance et fidélisation
            - >1 commandes → Objectif : relation durable, ventes répétées, augmentation du panier moyen
        """
        order_count = self.ventes.count()  # Nombre de ventes liées à ce client

        if order_count == 0:
            return {
                "label": "Prospect",
                "objectif": "Convertir en premier achat",
                "color": "secondary"
            }
        elif order_count == 1:
            return {
                "label": "Nouveau Client",
                "objectif": "Réassurance et fidélisation",
                "color": "primary"
            }
        else:
            return {
                "label": "Client Fidèle",
                "objectif": "Relation durable, ventes répétées, augmentation du panier moyen",
                "color": "success"
            }
