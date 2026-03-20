from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'status', 'link_clicked', 'sent_at')
    list_filter = ('status', 'link_clicked', 'sent_at')
    readonly_fields = ('sent_at',) # باش ما تبدلش وقت الإرسال بيدك