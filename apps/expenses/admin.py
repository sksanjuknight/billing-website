from django.contrib import admin
from .models import Expense, Payment

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'category', 'description', 'amount', 'user']
    list_filter = ['category', 'date', 'created_at']
    search_fields = ['description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Expense Info', {
            'fields': ('user', 'category', 'description', 'amount', 'date')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['date', 'customer', 'amount', 'payment_method', 'user']
    list_filter = ['payment_method', 'date', 'created_at']
    search_fields = ['customer__name', 'reference_number', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'customer', 'amount', 'date', 'payment_method')
        }),
        ('Reference', {
            'fields': ('reference_number', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
