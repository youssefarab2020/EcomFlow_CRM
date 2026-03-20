from django.db import models
from apps.clients.models import Client
from apps.products.models import Product
from apps.automations.models import Automation

class Interaction(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('replied', 'Replied'),
        ('interested', 'Interested'),
        ('purchased', 'Purchased'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    automation = models.ForeignKey(Automation, on_delete=models.SET_NULL, null=True)
    
    # المحتوى والنتائج
    message_sent = models.TextField()
    client_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    
    # التتبع (The Killing Feature)
    link_clicked = models.BooleanField(default=False)
    ai_sentiment = models.CharField(max_length=50, blank=True, help_text="تحليل رد العميل (إيجابي/سلبي)")
    
    sent_at = models.DateTimeField(auto_now_add=True)
    response_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Interaction with {self.client.name} - {self.status}"