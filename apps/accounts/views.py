from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm
from .models import User


# ===========================
# (1) INSCRIPTION UTILISATEUR (REGISTER)
# ===========================
def register_view(request):

    # (1.1) Cas POST : envoi du formulaire
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            # (1.2) Message de succès après création du compte
            messages.success(request, "Compte créé avec succès !")

            return redirect('accounts:login')

        else:
            # (1.3) Debug des erreurs (utile en développement)
            print(form.errors)

    # (1.4) Cas GET : affichage du formulaire vide
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ===========================
# (2) CONNEXION UTILISATEUR (LOGIN)
# ===========================
class UserLoginView(LoginView):

    # (2.1) Template utilisé pour le login
    template_name = 'accounts/login.html'

    # (2.2) Redirection si déjà connecté
    redirect_authenticated_user = True

    # (2.3) Redirection après connexion réussie
    def get_success_url(self):
        return reverse_lazy('clients:list')


# ===========================
# (3) DÉCONNEXION UTILISATEUR (LOGOUT)
# ===========================
class UserLogoutView(LogoutView):

    # (3.1) Page de redirection après logout
    next_page = reverse_lazy('accounts:login')


# ===========================
# (4) PAGE D'ACCUEIL (INDEX)
# ===========================
def index(request):

    # (4.1) Si utilisateur connecté → redirection dashboard clients
    if request.user.is_authenticated:
        return redirect('clients:list')

    # (4.2) Sinon → page d'accueil publique
    return render(request, 'index.html')


# ===========================
# (5) MISE À JOUR DU PROFIL UTILISATEUR
# ===========================
class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    # (5.1) Modèle utilisé
    model = User

    # (5.2) Formulaire de mise à jour
    form_class = ProfileUpdateForm

    # (5.3) Template associé
    template_name = 'accounts/profile_edit.html'

    # (5.4) Redirection après succès
    success_url = reverse_lazy('clients:list')

    # (5.5) Récupération de l'utilisateur connecté
    def get_object(self):
        return self.request.user

    # (5.6) Message de confirmation après modification
    def form_valid(self, form):
        messages.success(
            self.request,
            "Votre profil a été mis à jour avec succès !"
        )
        return super().form_valid(form)