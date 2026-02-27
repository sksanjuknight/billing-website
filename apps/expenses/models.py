from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from apps.customers.models import Customer

class Expense(models.Model):
    """Expense tracking model"""
    EXPENSE_CATEGORY_CHOICES = [
        ('raw_material', 'Raw Material'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('packaging', 'Packaging'),
        ('transport', 'Transport'),
        ('labour', 'Labour'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"

class Payment(models.Model):
    """Payment received from customers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('check', 'Check'),
            ('bank_transfer', 'Bank Transfer'),
            ('upi', 'UPI'),
            ('credit_card', 'Credit Card'),
        ],
        default='cash'
    )
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment - {self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        """Update customer balance when payment is saved"""
        super().save(*args, **kwargs)
        if self.customer:
            self.customer.update_balance()
