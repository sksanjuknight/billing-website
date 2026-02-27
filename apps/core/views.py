from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Q
from django.utils import timezone
from datetime import timedelta
from apps.billing.models import Invoice
from apps.expenses.models import Payment, Expense
from apps.labour.models import Labour, Attendance

@login_required
def dashboard(request):
    """Dashboard with business summary"""
    user = request.user
    
    # Get current month dates
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # Calculate totals
    total_sales = Invoice.objects.filter(user=user).aggregate(
        total=Sum('grand_total')
    )['total'] or 0
    
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_payments_received = Payment.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Current month data
    month_sales = Invoice.objects.filter(
        user=user,
        invoice_date__gte=month_start
    ).aggregate(total=Sum('grand_total'))['total'] or 0
    
    month_expenses = Expense.objects.filter(
        user=user,
        date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    profit = total_sales - total_expenses
    month_profit = month_sales - month_expenses
    
    # Recent invoices
    recent_invoices = Invoice.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_payments': total_payments_received,
        'profit': profit,
        'month_sales': month_sales,
        'month_expenses': month_expenses,
        'month_profit': month_profit,
        'recent_invoices': recent_invoices,
    }
    
    return render(request, 'dashboard.html', context)
