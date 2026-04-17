
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    # --- حقول موروثة تلقائياً (موجودة أصلاً في AbstractUser) ---
    # username   -> (CharField) موجود تلقائياً
    # password   -> (CharField) موجود تلقائياً ومحمي بتشفير
    # last_login -> (DateTimeField) موجود تلقائياً، يسجل وقت آخر دخول
    # date_joined-> (DateTimeField) موجود تلقائياً، يسجل وقت إنشاء الحساب
    # is_active  -> (BooleanField) موجود تلقائياً، لتفعيل أو تعطيل الحساب

    # --- حقول قمنا بتعديلها أو إضافتها (Custom Fields) ---

    # قمنا بإضافة unique=True لنجعله أساسياً في تسجيل الدخول
    email = models.EmailField(unique=True, verbose_name="Adresse Email")

    # حقول الـ CRM الخاصة بك
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nom de l'entreprise")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    
    # حقل اللوجو مع تنظيم التاريخ داخل مجلد media
    logo = models.ImageField(
        upload_to='logos/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name="Logo d'entreprise"
    )

    # --- إعدادات نظام الهوية ---
    
    # نخبر Django أن الإيميل هو "مفتاح" الدخول بدلاً من اليوزر نيم
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.username