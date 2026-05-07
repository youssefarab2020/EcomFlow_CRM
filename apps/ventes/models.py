from django.db import models , transaction
from apps.clients.models import Client
from apps.products.models import Product
from django.conf import settings
from django.db import models
class Vente(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # (1) Relation avec le client
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ventes')

    # (2) Relation avec le produit
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ventes')

    # (3) Quantité vendue
    quantity = models.PositiveIntegerField(default=1)

    # (4) Prix au moment de la vente (optionnel → prend le prix du produit automatiquement)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # (5) Montant total calculé automatiquement
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # (6) Date de création
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # (8) Définir le prix automatiquement si vide
        if not self.price:
            self.price = self.product.price

        # (9) Calcul du total
        self.total_amount = self.price * self.quantity

        # (10) Réduire le stock uniquement lors de la création
        if not self.pk:
            self.product.stock -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)
  
    # (1) Redéfinition de la méthode delete pour gérer le stock automatiquement
    def delete(self, *args, **kwargs):
        
        # (2) Récupérer le produit associé à cette vente
        product = self.product
        
        # (3) Réajouter la quantité vendue au stock du produit
        product.stock += self.quantity
        
        # (4) Sauvegarder la mise à jour du stock dans la base de données
        product.save()

        # (5) Appeler la méthode delete originale pour supprimer définitivement la vente
        super().delete(*args, **kwargs)

    def update_quantite(self, nouvelle_qte, ancienne_qte):
        """
        (FR) Mise à jour de la quantité et du stock en utilisant l'ancienne valeur.
        """
        if nouvelle_qte <= 0:
            raise ValueError("La quantité doit être supérieure à zéro.")

        # (Calcul du Delta réel)
        delta = nouvelle_qte - ancienne_qte

        # Vérification du stock en cas d'augmentation
        if delta > 0 and self.product.stock < delta:
            raise ValueError(f"Stock insuffisant ! Il manque {delta - self.product.stock} unités.")

        # (IMPORTANT) Mise à jour du tableau PRODUIT
        product = self.product
        product.stock -= delta
        product.save() # C'est ici que le stock change réellement dans la DB

        # Mise à jour du tableau VENTE
        self.quantity = nouvelle_qte
        self.save()


    def __str__(self):
        # (11) Affichage dans l’admin
        return f"{self.client.name} | {self.product.name} ({self.quantity})"

    class Meta:
        # (12) Trier du plus récent au plus ancien
        ordering = ['-created_at']
       
