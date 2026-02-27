from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.utils import timezone
import json
from apps.billing.models import Invoice
from apps.expenses.models import Expense, Payment
from apps.labour.models import Wage


@login_required
def dashboard_reports(request):
    """Main reports dashboard"""
    user = request.user
    today = timezone.now().date()
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_type = request.GET.get('type', 'monthly')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = today.replace(day=1)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = today
    
    invoices = Invoice.objects.filter(
        user=user,
        invoice_date__gte=start_date,
        invoice_date__lte=end_date
    )
    
    expenses = Expense.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    total_sales = invoices.aggregate(total=Sum('grand_total'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    profit = total_sales - total_expenses
    profit_margin = (profit / total_sales * 100) if total_sales > 0 else 0
    
    expenses_by_category = expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    expenses_by_category_list = []
    for item in expenses_by_category:
        percent = (item['total'] / total_expenses * 100) if total_expenses > 0 else 0
        expenses_by_category_list.append({
            'category': item['category'],
            'total': item['total'],
            'percent': round(percent, 2)
        })
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'report_type': report_type,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'profit_margin': profit_margin,
        'invoice_count': invoices.count(),
        'expense_count': expenses.count(),
        'expenses_by_category': expenses_by_category_list,
    }
    
    return render(request, 'reports/dashboard.html', context)


@login_required
def profit_loss_report(request):
    """Profit and Loss report with monthly grouping for chart"""
    user = request.user
    today = timezone.now().date()
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = today.replace(day=1)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = today
    
    invoices = Invoice.objects.filter(
        user=user,
        invoice_date__gte=start_date,
        invoice_date__lte=end_date
    )
    
    expenses = Expense.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Totals
    gross_sales = invoices.aggregate(total=Sum('grand_total'))['total'] or 0
    gst_collected = invoices.aggregate(total=Sum('gst_total'))['total'] or 0
    net_sales = gross_sales - gst_collected
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # Expenses by category
    expenses_by_category = {}
    for choice_code, choice_name in Expense.EXPENSE_CATEGORY_CHOICES:
        category_total = expenses.filter(
            category=choice_code
        ).aggregate(total=Sum('amount'))['total'] or 0
        expenses_by_category[choice_name] = category_total
    
    profit = net_sales - total_expenses
    profit_percentage = (profit / net_sales * 100) if net_sales > 0 else 0
    
    # ----------------------------
    # MONTHLY GROUPING (FIXED)
    # ----------------------------
    
    monthly_sales = (
        invoices
        .annotate(month=TruncMonth('invoice_date'))
        .values('month')
        .annotate(
            monthly_sales=Sum('grand_total'),
            monthly_gst=Sum('gst_total')
        )
        .annotate(
            monthly_net_sales=ExpressionWrapper(
                F('monthly_sales') - F('monthly_gst'),
                output_field=DecimalField()
            )
        )
        .order_by('month')
    )
    
    monthly_expenses = (
        expenses
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    
    monthly_profits = {}
    
    # Add sales months
    for entry in monthly_sales:
        month_key = entry['month'].strftime('%Y-%m')
        monthly_profits[month_key] = float(entry['monthly_net_sales'] or 0)
    
    # Add expense months (even if no sales in that month)
    for entry in monthly_expenses:
        month_key = entry['month'].strftime('%Y-%m')
        expense_amount = float(entry['total'] or 0)
        
        if month_key in monthly_profits:
            monthly_profits[month_key] -= expense_amount
        else:
            monthly_profits[month_key] = -expense_amount
    
    # Sort months
    monthly_profits = dict(sorted(monthly_profits.items()))
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'gross_sales': gross_sales,
        'gst_collected': gst_collected,
        'net_sales': net_sales,
        'total_expenses': total_expenses,
        'expenses_by_category': expenses_by_category,
        'profit': profit,
        'profit_percentage': profit_percentage,
        'monthly_profits_json': json.dumps(monthly_profits),
    }
    
    return render(request, 'reports/profit_loss.html', context)


@login_required
def sales_report(request):
    """Sales analysis report"""
    user = request.user
    today = timezone.now().date()
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = today.replace(day=1)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = today
    
    invoices = Invoice.objects.filter(
        user=user,
        invoice_date__gte=start_date,
        invoice_date__lte=end_date
    )
    
    daily_sales = {}
    current_date = start_date
    while current_date <= end_date:
        daily_total = invoices.filter(
            invoice_date=current_date
        ).aggregate(total=Sum('grand_total'))['total'] or 0
        daily_sales[current_date.strftime('%Y-%m-%d')] = float(daily_total)
        current_date += timedelta(days=1)
    
    customer_sales = invoices.values('customer__name').annotate(
        total=Sum('grand_total')
    ).order_by('-total')[:10]
    
    total_sales = invoices.aggregate(total=Sum('grand_total'))['total'] or 0
    average_daily_sales = total_sales / max((end_date - start_date).days + 1, 1)
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'daily_sales': json.dumps(daily_sales),
        'customer_sales': customer_sales,
        'total_sales': total_sales,
        'average_daily_sales': average_daily_sales,
        'invoice_count': invoices.count(),
    }
    
    return render(request, 'reports/sales.html', context)


@login_required
def labour_report(request):
    """Labour and wage report"""
    user = request.user
    today = timezone.now().date()
    
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    wages = Wage.objects.filter(
        labour__user=user,
        year=year,
        month=month
    ).order_by('labour__name')
    
    total_wages_paid = wages.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'year': year,
        'month': month,
        'wages': wages,
        'total_wages_paid': total_wages_paid,
    }
    
    return render(request, 'reports/labour.html', context)