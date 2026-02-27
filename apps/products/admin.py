from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'mrp', 'retail_price', 'gst_rate', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'image', 'description')
        }),
        ('Pricing', {
            'fields': ('mrp', 'retail_price', 'wholesale_price')
        }),
        ('Dates & Tax', {
            'fields': ('manufacture_date', 'expiry_date', 'gst_rate', 'hsn_code')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
