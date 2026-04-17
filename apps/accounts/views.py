from django.shortcuts import render, redirect 

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import CustomUserChangeForm
# --- 1. عرض صفحة إنشاء حساب (Sign Up) ---
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import CustomUserCreationForm
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé !")
            return redirect('accounts:login')
        else:
            # هذا السطر سيطبع لك الخطأ في شاشة الـ VS Code/Terminal
            print(form.errors) 
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
# --- 2. عرض صفحة تسجيل الدخول (Login) ---
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True  # إذا كان مسجلاً دخولاً بالفعل، انقله للصفحة الرئيسية
    
    def get_success_url(self):
        # يمكنك تغيير 'home' إلى اسم رابط لوحة التحكم (Dashboard) الخاصة بك
        return reverse_lazy('clients:list') 


# --- 3. تسجيل الخروج (Logout) ---
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login') # التوجه لصفحة الدخول بعد الخروج


    
def index(request):
    # إذا كان المستخدم مسجل دخوله بالفعل
    if request.user.is_authenticated:
        return redirect('clients:list') # وجهه لصفحة العملاء
    
    # إذا لم يكن مسجلاً، اظهر له صفحة الهبوط العادية
    return render(request, 'index.html')
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ProfileUpdateForm

from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ProfileUpdateForm 
from .models import User # تأكد من استيراد الموديل الخاص بك

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('clients:list')

    # هذه الدالة تجلب بيانات المستخدم المسجل حالياً لملء الخانات بها
    def get_object(self):
        return self.request.user

    # هذه الدالة تظهر رسالة النجاح عند الحفظ
    def form_valid(self, form):
        messages.success(self.request, "Votre profil a été mis à jour avec succès !")
        return super().form_valid(form)