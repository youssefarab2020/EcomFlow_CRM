from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # (1) Liste des colonnes affichées dans l'administration
    list_display = (
        'name', 
        'sku', 
        'price', 
        'cost_price', 
        'get_profit_admin',  # Affichage de la marge
        'stock', 
        'stock_status',      # Indicateur visuel du stock
        'created_at'
    )

    # (2) Filtres latéraux pour une navigation rapide
    list_filter = ('created_at', 'stock')

    # (3) Champs de recherche (Nom et SKU)
    search_fields = ('name', 'sku')

    # (4) Organisation des formulaires de saisie
    fieldsets = (
        ('Informations Générales', {
            'fields': ('name', 'sku', 'description')
        }),
        ('Prix & Finance', {
            'fields': ('price', 'cost_price')
        }),
        ('Gestion du Stock', {
            'fields': ('stock',)
        }),
    )

    # (5) Fonction pour afficher la marge dans l'admin
    def get_profit_admin(self, obj):
        return f"{obj.get_margin()} $"
    get_profit_admin.short_description = 'Marge Bénéficiaire' # Nom de la colonne

    # (6) Fonction pour un indicateur visuel du stock
    def stock_status(self, obj):
        if obj.stock <= 0:
            return "❌ Rupture"
        elif obj.stock <= 5:
            return "⚠️ Stock Bas"
        return "✅ En Stock"
    stock_status.short_description = 'État du Stock'