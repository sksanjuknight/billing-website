from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Labour(models.Model):
    """Labour/Worker model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Labour"

    def __str__(self):
        return self.name

    def get_month_summary(self, year, month):
        """Get monthly attendance and payment summary"""
        from datetime import datetime, timedelta
        
        # Get first and last day of month
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        # Get all attendance records for this month
        attendances = Attendance.objects.filter(
            labour=self,
            date__gte=start_date,
            date__lte=end_date,
            present=True
        ).count()
        
        total_payment = attendances * self.daily_wage
        
        return {
            'days_worked': attendances,
            'total_payment': total_payment,
            'daily_wage': self.daily_wage,
        }

class Attendance(models.Model):
    """Daily attendance record"""
    labour = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['labour', 'date']
        ordering = ['-date']
        verbose_name_plural = "Attendance"

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.labour.name} - {self.date} - {status}"

class Wage(models.Model):
    """Track wages paid to labour"""
    labour = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='wages')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date_paid = models.DateField()
    month = models.IntegerField()  # Month (1-12)
    year = models.IntegerField()   # Year
    days_worked = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['labour', 'month', 'year']
        ordering = ['-year', '-month']
        verbose_name_plural = "Wages"

    def __str__(self):
        return f"{self.labour.name} - {self.month}/{self.year} - {self.amount}"
