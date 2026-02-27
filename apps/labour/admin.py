from django.contrib import admin
from .models import Labour, Attendance, Wage

@admin.register(Labour)
class LabourAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'daily_wage', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'name', 'phone', 'address')
        }),
        ('Wages', {
            'fields': ('daily_wage',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['labour', 'date', 'present']
    list_filter = ['present', 'date']
    search_fields = ['labour__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Wage)
class WageAdmin(admin.ModelAdmin):
    list_display = ['labour', 'year', 'month', 'days_worked', 'amount']
    list_filter = ['year', 'month']
    search_fields = ['labour__name']
    readonly_fields = ['created_at']
