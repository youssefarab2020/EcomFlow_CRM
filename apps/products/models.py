from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=255)                 # (1) Nom du produit

    sku = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )                                                       # (2) Code produit (optionnel)

    price = models.DecimalField(max_digits=10, decimal_places=2)  # (3) Prix de vente

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )                                                       # (4) Prix de coût (optionnel)

    stock = models.PositiveIntegerField(default=0)          # (5) Quantité disponible

    description = models.TextField(blank=True)              # (6) Description

    created_at = models.DateTimeField(auto_now_add=True)    # (7) Date de création

    def __str__(self):
        return self.name if not self.sku else f"{self.name} [{self.sku}]"  # (8) Affichage propre

    class Meta:
        ordering = ['-created_at']                          # (9) Trier du plus récent

    # --- (10) FONCTIONS ESSENTIELLES ---

    def get_margin(self):
        """Calcule la marge bénéficiaire par unité"""
        return self.price - self.cost_price                 # (10.1) Calcul de la marge brute

    def get_total_stock_value(self):
        """Calcule la valeur totale du stock (Prix de vente x Quantité)"""
        return self.price * self.stock                      # (10.2) Valeur marchande du stock

    def is_low_stock(self, limit=5):
        """Vérifie si le stock est bas (Alerte)"""
        return self.stock <= limit                          # (10.3) Alerte de stock faible

    def has_stock(self):
        """Vérifie si le produit est disponible"""
        return self.stock > 0                               # (10.4) Disponibilité du produit