from django.db import models

class Client(models.Model):
    # خيارات الحالة (Status Choices)
    STATUS_CHOICES = [
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('churn', 'Churned'),
    ]

    # المعلومات الأساسية
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, help_text="Example: +212600000000")
    email = models.EmailField(unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    
    # بيانات البيزنس (Smart Fields)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_purchase = models.DateTimeField(null=True, blank=True)
    
    # توقيت التسجيل
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # هادي هي اللي كتخلي العميل يبان بسميتو وحالته فالـ Admin
        return f"{self.name} ({self.status})"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at'] # باش يبانو الجداد هما اللولين