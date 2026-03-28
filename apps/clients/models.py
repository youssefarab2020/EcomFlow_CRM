from django.db import models  # (1) Import du module models

class Client(models.Model):
    # (2) Nom du client
    name = models.CharField(max_length=255)

    # (3) Numéro de téléphone (avec exemple affiché)
    phone = models.CharField(max_length=20, help_text="Example: +212600000000")

    # (4) Email unique (optionnel)
    email = models.EmailField(unique=True, blank=True, null=True)

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