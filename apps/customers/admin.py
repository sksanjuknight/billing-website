from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone', 'customer_type', 'balance', 'is_active']
    list_filter = ['customer_type', 'is_active', 'created_at']
    search_fields = ['name', 'phone', 'user__username']
    readonly_fields = ['total_billed', 'total_paid', 'balance', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'phone', 'email')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Business Info', {
            'fields': ('customer_type', 'gst_number', 'is_active')
        }),
        ('Financial Summary', {
            'fields': ('total_billed', 'total_paid', 'balance')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
