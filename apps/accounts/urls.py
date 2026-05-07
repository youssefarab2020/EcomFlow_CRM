from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views


# ===========================
# (1) NOM DE L'APPLICATION
# ===========================
# Permet d'organiser les routes et d'éviter les conflits entre apps
app_name = 'accounts'


# ===========================
# (2) DÉFINITION DES ROUTES
# ===========================
urlpatterns = [

    # (2.1) Page d'accueil / index du module accounts
    path('', views.index, name='index'),

    # (2.2) Page d'inscription utilisateur
    path('register/', views.register_view, name='register'),

    # (2.3) Page de modification du profil utilisateur (CBV)
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

    # (2.4) Connexion utilisateur (Login personnalisé)
    path('login/', views.UserLoginView.as_view(), name='login'),

    # (2.5) Déconnexion utilisateur (redirige vers login après logout)
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='accounts:login'),
        name='logout'
    ),
]


# ===========================
# (3) CONFIGURATION MEDIA (DÉVELOPPEMENT UNIQUEMENT)
# ===========================
# Permet l'affichage des images (logo, avatars...) en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)