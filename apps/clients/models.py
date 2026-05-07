from django.db import models  # (1) Import du module models
from django.conf import settings  # (2) Accès au modèle User personnalisé


class Client(models.Model):
    # (3) Lien avec l'utilisateur (multi-tenant : chaque client appartient à un user)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # (4) Nom du client
    name = models.CharField(max_length=255)

    # (5) Numéro de téléphone avec exemple
    phone = models.CharField(max_length=20, help_text="Example: +212600000000")

    # (6) Email optionnel (unicité gérée par contrainte)
    email = models.EmailField(blank=True, null=True)

    # (7) Ville du client (optionnelle)
    city = models.CharField(max_length=100, blank=True)

    # (8) Date de création automatique
    created_at = models.DateTimeField(auto_now_add=True)

    # (9) Représentation lisible dans l’admin Django
    def __str__(self):
        return self.name

    # (10) Configuration globale du modèle
    class Meta:
        # (11) Trier les clients du plus récent au plus ancien
        ordering = ['-created_at']

        # (12) Contrainte : un email doit être unique pour chaque utilisateur
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'email'],
                name='unique_client_email_per_user'
            )
        ]

    # (13) Propriété calculée pour définir la stratégie marketing
    @property
    def marketing_status(self):
        # (14) Calculer le nombre de ventes liées à ce client
        order_count = self.ventes.count()

        # (15) Aucun achat → Prospect
        if order_count == 0:
            return {
                "label": "Prospect",
                "objectif": "Convertir en premier achat",
                "color": "secondary"
            }

        # (16) Un seul achat → Nouveau client
        elif order_count == 1:
            return {
                "label": "Nouveau Client",
                "objectif": "Réassurance et fidélisation",
                "color": "primary"
            }

        # (17) Plusieurs achats → Client fidèle
        return {
            "label": "Client Fidèle",
            "objectif": "Relation durable, ventes répétées, augmentation du panier moyen",
            "color": "success"
        }