from django.contrib import admin
from .models import Vente

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    # (1) الأعمدة التي ستظهر في الجدول الرئيسي
    list_display = ('id', 'client', 'product', 'quantity', 'price', 'total_amount', 'created_at')
    
    # (2) إضافة فلاتر جانبية للبحث السريع
    list_filter = ('created_at', 'client', 'product')
    
    # (3) تفعيل البحث بالاسم أو المنتج
    search_fields = ('client__name', 'product__name')
    
    # (4) جعل الحقول المحسوبة "للقراءة فقط" في صفحة التعديل لعدم تخريب الحسابات
    readonly_fields = ('total_amount', 'created_at')
    
    # (5) تقسيم الحقول إلى مجموعات داخل صفحة الإضافة (اختياري لجمالية التصميم)
    fieldsets = (
        ('Informations Client & Produit', {
            'fields': ('client', 'product')
        }),
        ('Détails de la Vente', {
            'fields': ('quantity', 'price')
        }),
        ('Calculs Automatiques', {
            'fields': ('total_amount', 'created_at'),
            'description': "Ces champs sont calculés automatiquement par le système."
        }),
    )

    # (6) دالة لإضافة لون مميز للمبالغ الكبيرة (اختياري)
    def total_amount_display(self, obj):
        return f"{obj.total_amount} DH"
    total_amount_display.short_description = "Montant Total"