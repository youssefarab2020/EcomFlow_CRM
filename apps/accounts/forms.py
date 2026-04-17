from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


# --- Formulaire pour l'inscription (Création d'utilisateur) ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Ajout des nouveaux champs au formulaire d'inscription
        fields = ('email', 'username', 'company_name', 'phone_number', 'address', 'logo')

    # Optionnel: Personnalisation des widgets pour un meilleur design
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# --- Formulaire pour la modification (Edition d'utilisateur) ---
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'company_name', 'phone_number', 'address', 'logo', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On peut désactiver certains champs si nécessaire
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
from django import forms
from .models import User # استيراد موديل اليوزر الخاص بك

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # لاحظ أنني أزلت first_name و last_name لأنك لم تضفها في الموديل الخاص بك صراحة، 
        # (رغم أنها موجودة في AbstractUser لكن لنتجنب أي خطأ، سنكتفي بما هو موجود لديك)
        fields = ['username', 'email', 'company_name', 'phone_number', 'address', 'logo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})