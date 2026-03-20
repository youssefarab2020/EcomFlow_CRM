from django.db import models

class Automation(models.Model):
    TRIGGER_TYPES = [
        ('after_signup', 'After Signup'),
        ('after_purchase', 'After Purchase'),
        ('inactive_reminder', 'Inactive Reminder'),
        ('cart_abandoned', 'Cart Abandoned'),
    ]

    name = models.CharField(max_length=100)
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    message_template = models.TextField(help_text="القالب الأساسي للرسالة")
    
    # التوقيت البشري (Human-like Logic)
    delay_hours = models.PositiveIntegerField(default=0)
    working_hours_start = models.TimeField(default="09:00")
    working_hours_end = models.TimeField(default="22:00")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.trigger_type})"