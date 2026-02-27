from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'user', 'customer', 'grand_total', 'status', 'invoice_date']
    list_filter = ['status', 'invoice_date', 'created_at']
    search_fields = ['invoice_number', 'user__username', 'customer__name']
    readonly_fields = ['invoice_number', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    fieldsets = (
        ('Invoice Info', {
            'fields': ('user', 'customer', 'invoice_number', 'invoice_date', 'status')
        }),
        ('Totals', {
            'fields': ('subtotal', 'gst_total', 'grand_total')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'invoice', 'quantity', 'price_per_unit', 'line_total']
    search_fields = ['item_name', 'invoice__invoice_number']
