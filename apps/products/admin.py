from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category')
    fieldsets = (
        ('المعلومات الأساسية', {'fields': ('name', 'price', 'category', 'description')}),
        ('التسويق (AI Context)', {'fields': ('target_audience', 'benefits', 'problem_solved')}),
        ('معالجة الاعتراضات', {'fields': ('common_objections', 'faq_context')}),
    )