from django.db import models
from django.contrib.auth.models import User

class BusinessProfile(models.Model):
    """Store business information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20)   # your main contact
    address = models.TextField()

    # ✅ ADD THESE (do not remove anything)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    contact_details = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name_plural = "Business Profiles"
