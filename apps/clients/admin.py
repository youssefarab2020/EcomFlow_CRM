from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'phone', 'email')