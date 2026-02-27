from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.products.models import Product
from apps.customers.models import Customer


class Invoice(models.Model):
    """GST-compliant Invoice model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    # Totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # NEW: track payments received
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Total amount actually paid by customer so far"
    )

    # Status - added 'partial'
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"Invoice {self.invoice_number}"

    @property
    def balance_due(self):
        """How much customer still owes"""
        return max(self.grand_total - self.amount_paid, Decimal('0.00'))

    @property
    def display_status(self):
        """Smart, human-friendly status based on actual payments"""
        if self.status == 'draft':
            return 'Draft'
        if self.balance_due <= 0:
            return 'Paid'
        if self.amount_paid > 0:
            return 'Partially Paid'
        return 'Unpaid'

    def update_status_from_payments(self):
        """Call after recording payment(s)"""
        if self.balance_due <= 0:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'
        self.save(update_fields=['status', 'amount_paid'])

    def calculate_totals(self):
        """Calculate invoice totals (NO recursive save)"""
        items = self.items.all()

        subtotal = Decimal('0.00')
        gst_total = Decimal('0.00')

        for item in items:
            subtotal += item.line_total
            gst_total += item.gst_amount

        self.subtotal = subtotal
        self.gst_total = gst_total
        self.grand_total = subtotal + gst_total

        # Update only calculated fields
        Invoice.objects.filter(pk=self.pk).update(
            subtotal=self.subtotal,
            gst_total=self.gst_total,
            grand_total=self.grand_total
        )


class InvoiceItem(models.Model):
    """Individual items in an invoice"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    # Calculated fields
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        """Calculate line totals and update invoice totals"""
        self.line_total = self.quantity * self.price_per_unit
        self.gst_amount = (self.line_total * self.gst_rate) / Decimal('100')
        super().save(*args, **kwargs)

        # Update invoice totals
        self.invoice.calculate_totals()

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"