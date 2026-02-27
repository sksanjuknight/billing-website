from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.db.models import Sum, Count
import calendar
from .models import Labour, Attendance, Wage

@login_required
def labour_list(request):
    """List all labour workers"""
    labour_list = Labour.objects.filter(user=request.user)
    return render(request, 'labour/labour_list.html', {'labour_list': labour_list})

@login_required
@require_http_methods(["GET", "POST"])
def labour_create(request):
    """Create a new labour worker"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            daily_wage = request.POST.get('daily_wage')
            
            if not all([name, daily_wage]):
                messages.error(request, 'Missing required fields: Name and Daily Wage are required.')
                return redirect('labour_create')
            
            labour = Labour.objects.create(
                user=request.user,
                name=name,
                daily_wage=daily_wage,
                phone=request.POST.get('phone', ''),
                address=request.POST.get('address', '')
            )
            
            messages.success(request, f'Worker "{labour.name}" added successfully!')
            return redirect('labour_list')
            
        except Exception as e:
            messages.error(request, f'Error adding worker: {str(e)}')
            return redirect('labour_create')
    
    return render(request, 'labour/labour_form.html')

@login_required
@require_http_methods(["GET", "POST"])
def labour_edit(request, pk):
    """Edit a labour worker"""
    labour = get_object_or_404(Labour, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            labour.name = request.POST.get('name', labour.name)
            labour.daily_wage = request.POST.get('daily_wage', labour.daily_wage)
            labour.phone = request.POST.get('phone', labour.phone)
            labour.address = request.POST.get('address', labour.address)
            labour.save()
            
            messages.success(request, f'Worker "{labour.name}" updated successfully!')
            return redirect('labour_list')
            
        except Exception as e:
            messages.error(request, f'Error updating worker: {str(e)}')
            return redirect('labour_edit', pk=pk)
    
    context = {'labour': labour}
    return render(request, 'labour/labour_form.html', context)

@login_required
def labour_detail(request, pk):
    """View labour details and attendance"""
    labour = get_object_or_404(Labour, pk=pk, user=request.user)
    
    # Get current month/year or selected from GET params
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Validate and set month boundaries
    try:
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)
    except ValueError:
        # Fallback to current month if invalid
        month_start = date(today.year, today.month, 1)
        month_end = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
        year, month = today.year, today.month

    # Attendance records for selected month
    attendances = Attendance.objects.filter(
        labour=labour,
        date__gte=month_start,
        date__lte=month_end
    ).order_by('date')

    # Calculate summary
    days_worked = attendances.filter(present=True).count()  # Full days only for now
    total_wages = Decimal(days_worked) * labour.daily_wage

    # Paid amount from Wage records in the same month
    paid_amount = Wage.objects.filter(
        labour=labour,
        date_paid__gte=month_start,
        date_paid__lte=month_end
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    balance_due = total_wages - paid_amount

    # Prepare dynamic year range for dropdown (current year ± 3)
    current_year = datetime.now().year
    available_years = list(range(current_year - 3, current_year + 4))

    context = {
        'labour': labour,
        'attendances': attendances,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_choices': [(str(i), calendar.month_name[i]) for i in range(1, 13)],
        'available_years': available_years,  # Added for safe year dropdown
        'summary': {
            'days_worked': days_worked,
            'total_wages': total_wages,
            'paid_amount': paid_amount,
            'balance_due': balance_due,
        },
    }
    return render(request, 'labour/labour_detail.html', context)

@login_required
@require_http_methods(["POST"])
def mark_attendance(request, pk):
    """Mark attendance for a labour worker"""
    labour = get_object_or_404(Labour, pk=pk, user=request.user)
    
    try:
        data = json.loads(request.body)
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        present = data.get('present', True)
        
        attendance, created = Attendance.objects.get_or_create(
            labour=labour,
            date=attendance_date,
            defaults={'present': present}
        )
        
        if not created:
            attendance.present = present
            attendance.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def labour_delete(request, pk):
    """Delete a labour worker"""
    labour = get_object_or_404(Labour, pk=pk, user=request.user)
    name = labour.name  # Capture name before deletion for message
    labour.delete()
    
    messages.success(request, f'Worker "{name}" deleted successfully!')
    return redirect('labour_list')

# Wage Management (optional - can be used for recording payments)

@login_required
def wage_summary(request):
    """View wage summary for all workers"""
    labour_list = Labour.objects.filter(user=request.user)
    
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    wage_data = []
    for labour in labour_list:
        month_start = date(year, month, 1)
        month_end = date(year, month, calendar.monthrange(year, month)[1])
        
        attendances = Attendance.objects.filter(
            labour=labour,
            date__gte=month_start,
            date__lte=month_end
        )
        
        days_worked = attendances.filter(present=True).count()
        total_wages = Decimal(days_worked) * labour.daily_wage
        
        paid_amount = Wage.objects.filter(
            labour=labour,
            date_paid__gte=month_start,
            date_paid__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        balance_due = total_wages - paid_amount
        
        wage_data.append({
            'labour': labour,
            'days_worked': days_worked,
            'total_wages': total_wages,
            'paid_amount': paid_amount,
            'balance_due': balance_due,
        })
    
    context = {
        'wage_data': wage_data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_choices': [(str(i), calendar.month_name[i]) for i in range(1, 13)],
    }
    return render(request, 'labour/wage_summary.html', context)

@login_required
@require_http_methods(["POST"])
def record_wage_payment(request):
    """Record wage payment for a labour worker"""
    try:
        data = json.loads(request.body)
        labour_id = data['labour_id']
        month = int(data['month'])
        year = int(data['year'])
        amount = Decimal(data['amount'])
        
        labour = get_object_or_404(Labour, pk=labour_id, user=request.user)
        
        Wage.objects.create(
            labour=labour,
            amount=amount,
            date_paid=date.today(),
            month=month,
            year=year,
            days_worked=0,  # Can be updated later if needed
            notes=data.get('notes', '')
        )
        
        messages.success(request, f'Payment of ₹{amount} recorded for {labour.name}!')
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)