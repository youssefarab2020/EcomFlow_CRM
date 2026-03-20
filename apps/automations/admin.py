from django.contrib import admin
from .models import Automation

@admin.register(Automation)
class AutomationAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_type', 'is_active', 'delay_hours')
    list_editable = ('is_active',)