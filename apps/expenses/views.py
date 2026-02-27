from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from datetime import datetime
from .models import Expense, Payment
from apps.customers.models import Customer

@login_required
def expense_list(request):
    """List all expenses"""
    expenses = Expense.objects.filter(user=request.user)
    
    # Get summary
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
    }
    return render(request, 'expenses/expense_list.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def expense_create(request):
    """Create a new expense"""
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            description = request.POST.get('description')
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            
            if not all([category, description, amount, date]):
                messages.error(request, 'Missing required fields: Category, Description, Amount, and Date are required.')
                return redirect('expense_create')
            
            expense = Expense.objects.create(
                user=request.user,
                category=category,
                description=description,
                amount=amount,
                date=datetime.strptime(date, '%Y-%m-%d').date(),
                notes=request.POST.get('notes', '')
            )
            
            messages.success(request, f'Expense of ₹{expense.amount} added successfully!')
            return redirect('expense_list')  # ← changed: redirect instead of JsonResponse
            
        except Exception as e:
            messages.error(request, f'Error creating expense: {str(e)}')
            return redirect('expense_create')
    
    context = {
        'categories': Expense.EXPENSE_CATEGORY_CHOICES,
    }
    return render(request, 'expenses/expense_form.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def expense_edit(request, pk):
    """Edit an expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            expense.category = request.POST.get('category', expense.category)
            expense.description = request.POST.get('description', expense.description)
            expense.amount = request.POST.get('amount', expense.amount)
            expense.date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
            expense.notes = request.POST.get('notes', expense.notes)
            expense.save()
            
            messages.success(request, f'Expense updated successfully!')
            return redirect('expense_list')  # ← changed: redirect instead of JsonResponse
            
        except Exception as e:
            messages.error(request, f'Error updating expense: {str(e)}')
            return redirect('expense_edit', pk=pk)
    
    context = {
        'expense': expense,
        'categories': Expense.EXPENSE_CATEGORY_CHOICES,
    }
    return render(request, 'expenses/expense_form.html', context)

@login_required
@require_http_methods(["POST"])
def expense_delete(request, pk):
    """Delete an expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return JsonResponse({'success': True})

# Payment views

@login_required
def payment_list(request):
    """List all payments"""
    payments = Payment.objects.filter(user=request.user)
    total_received = payments.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payments': payments,
        'total_received': total_received,
    }
    return render(request, 'expenses/payment_list.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def payment_create(request):
    """Record a new payment"""
    if request.method == 'POST':
        try:
            customer_id = request.POST.get('customer')
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            
            if not all([customer_id, amount, date]):
                messages.error(request, 'Missing required fields: Customer, Amount, and Date are required.')
                return redirect('payment_create')
            
            customer = Customer.objects.get(id=customer_id, user=request.user)
            
            payment = Payment.objects.create(
                user=request.user,
                customer=customer,
                amount=amount,
                date=datetime.strptime(date, '%Y-%m-%d').date(),
                payment_method=request.POST.get('payment_method', 'cash'),
                reference_number=request.POST.get('reference_number', ''),
                notes=request.POST.get('notes', '')
            )
            
            messages.success(request, f'Payment of ₹{payment.amount} recorded successfully!')
            return redirect('payment_list')  # ← changed: redirect instead of JsonResponse
            
        except Exception as e:
            messages.error(request, f'Error recording payment: {str(e)}')
            return redirect('payment_create')
    
    customers = Customer.objects.filter(user=request.user)
    context = {
        'customers': customers,
    }
    return render(request, 'expenses/payment_form.html', context)

@login_required
@require_http_methods(["POST"])
def payment_delete(request, pk):
    """Delete a payment"""
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    payment.delete()
    return JsonResponse({'success': True})
    
