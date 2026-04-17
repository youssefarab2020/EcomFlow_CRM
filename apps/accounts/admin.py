from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. Personnalisation des champs affichés dans la liste des utilisateurs
    list_display = ('email', 'username', 'company_name', 'phone_number', 'is_staff')
    
    # 2. Ajout de filtres pour faciliter la recherche
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # 3. Définition des champs de recherche
    search_fields = ('email', 'username', 'company_name', 'phone_number')
    
    # 4. Ordre d'affichage (les plus récents en premier)
    ordering = ('-date_joined',)

    # 5. Personnalisation des sections dans la page de modification
    fieldsets = UserAdmin.fieldsets + (
        ('Informations CRM', {'fields': ('company_name', 'phone_number', 'address', 'logo')}),
    )
    
    # 6. Ajout des nouveaux champs lors de la création d'un utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Supplémentaires', {'fields': ('email', 'company_name', 'phone_number', 'address', 'logo')}),
    )

# Enregistrement du modèle avec la configuration personnalisée
admin.site.register(User, CustomUserAdmin)