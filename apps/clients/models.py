from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, help_text="Example: +212600000000")
    email = models.EmailField(unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']