from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    # ===========================
    # (1) CHAMPS NATIFS DJANGO (hérités automatiquement)
    # ===========================

    # username    -> identifiant utilisateur (géré par Django)
    # password    -> mot de passe crypté automatiquement
    # last_login  -> date de dernière connexion
    # date_joined -> date de création du compte
    # is_active   -> statut du compte (actif / désactivé)


    # ===========================
    # (2) CHAMPS PERSONNALISÉS CRM
    # ===========================

    # Adresse email unique utilisée pour l'authentification
    email = models.EmailField(unique=True, verbose_name="Adresse Email")

    # Nom de l'entreprise associée à l'utilisateur
    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nom de l'entreprise"
    )

    # Numéro de téléphone professionnel
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Numéro de téléphone"
    )

    # Adresse complète de l'utilisateur ou de l'entreprise
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse"
    )

    # Logo de l'entreprise avec organisation par date (media/logos/YYYY/MM/DD)
    logo = models.ImageField(
        upload_to='logos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Logo d'entreprise"
    )


    # ===========================
    # (3) CONFIGURATION AUTHENTIFICATION
    # ===========================

    # Utiliser l'email comme identifiant principal au lieu du username
    USERNAME_FIELD = 'email'

    # Champs obligatoires lors de la création d’un superuser
    REQUIRED_FIELDS = ['username']


    # ===========================
    # (4) REPRÉSENTATION DE L'OBJET
    # ===========================

    # Retourne le username lors de l'affichage de l'utilisateur
    def __str__(self):
        return self.username