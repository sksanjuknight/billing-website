from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Customer(models.Model):
    """Customer model for parties/customers"""
    CUSTOMER_TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('both', 'Both'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Customer info
    gst_number = models.CharField(max_length=20, blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='retail')
    
    # Financial info
    total_billed = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

    def update_balance(self):
        """Update customer balance"""
        from apps.billing.models import Invoice
        from apps.expenses.models import Payment
        
        total_billed = Invoice.objects.filter(
            customer=self
        ).aggregate(total=models.Sum('grand_total'))['total'] or 0
        
        total_paid = Payment.objects.filter(
            customer=self
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        self.total_billed = total_billed
        self.total_paid = total_paid
        self.balance = total_billed - total_paid
        self.save()
