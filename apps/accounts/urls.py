from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

# اسم التطبيق الخاص بك (اختياري لكنه مفيد لتنظيم الروابط)
app_name = 'accounts' 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
    # استخدم UserLoginView بدلاً من auth_views.LoginView
    path('login/', views.UserLoginView.as_view(), name='login'), 
    
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
]

# ⚠️ إعداد هام جداً لكي تعمل الصور (اللوجو) أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)