from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'total_spent', 'created_at')
    list_filter = ('status', 'city')
    search_fields = ('name', 'phone')