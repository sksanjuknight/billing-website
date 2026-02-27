from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Product(models.Model):
    """Product model for snacks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    manufacture_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    hsn_code = models.CharField(max_length=20, blank=True)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
