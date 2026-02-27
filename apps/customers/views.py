from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from .models import Customer
from apps.billing.models import Invoice
from apps.expenses.models import Payment

@login_required
def customer_list(request):
    """List all customers with calculated billed and balance"""
    customers = Customer.objects.filter(user=request.user)
    
    # Calculate Total Billed and Current Balance for each customer
    customer_data = []
    for customer in customers:
        invoices = Invoice.objects.filter(customer=customer)
        
        total_billed = invoices.aggregate(grand_total__sum=Sum('grand_total'))['grand_total__sum'] or Decimal('0.00')
        total_paid = invoices.aggregate(amount_paid__sum=Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')
        
        # Balance = Opening Balance + Billed - Paid (if opening_balance exists)
        opening_balance = getattr(customer, 'opening_balance', Decimal('0.00'))
        current_balance = opening_balance + total_billed - total_paid
        
        customer_data.append({
            'customer': customer,
            'total_billed': total_billed,
            'current_balance': current_balance,
        })
    
    context = {
        'customer_data': customer_data,
    }
    return render(request, 'customers/customer_list.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def customer_create(request):
    """Create a new customer"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            
            if not all([name, phone, address]):
                messages.error(request, 'Missing required fields: Name, Phone and Address are required.')
                return redirect('customer_create')
            
            customer = Customer.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                address=address,
                email=request.POST.get('email', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                customer_type=request.POST.get('customer_type', 'retail')
            )
            
            messages.success(request, f'Customer "{customer.name}" added successfully!')
            return redirect('customer_list')  
            
        except Exception as e:
            messages.error(request, f'Error creating customer: {str(e)}')
            return redirect('customer_create')
    
    return render(request, 'customers/customer_form.html')

@login_required
@require_http_methods(["GET", "POST"])
def customer_edit(request, pk):
    """Edit a customer"""
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            customer.name = request.POST.get('name', customer.name)
            customer.phone = request.POST.get('phone', customer.phone)
            customer.address = request.POST.get('address', customer.address)
            customer.email = request.POST.get('email', customer.email)
            customer.city = request.POST.get('city', customer.city)
            customer.state = request.POST.get('state', customer.state)
            customer.customer_type = request.POST.get('customer_type', customer.customer_type)
            customer.save()
            
            messages.success(request, f'Customer "{customer.name}" updated successfully!')
            return redirect('customer_list')  
            
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
            return redirect('customer_edit', pk=pk)
    
    context = {'customer': customer}
    return render(request, 'customers/customer_form.html', context)

@login_required
def customer_detail(request, pk):
    """View customer details and history"""
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    
    # Get all invoices for this customer
    invoices = Invoice.objects.filter(customer=customer)
    
    # Total Billed = sum of grand_total from all invoices
    total_billed = invoices.aggregate(grand_total__sum=Sum('grand_total'))['grand_total__sum'] or Decimal('0.00')
    
    # Total Paid = sum of amount_paid from all invoices
    total_paid = invoices.aggregate(amount_paid__sum=Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')
    
    # Current Balance = Opening Balance + Total Billed - Total Paid
    opening_balance = getattr(customer, 'opening_balance', Decimal('0.00'))
    current_balance = opening_balance + total_billed - total_paid
    
    payments = Payment.objects.filter(customer=customer)
    
    context = {
        'customer': customer,
        'invoices': invoices.order_by('-invoice_date'),
        'payments': payments,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'current_balance': current_balance,
    }
    return render(request, 'customers/customer_detail.html', context)

@login_required
@require_http_methods(["POST"])
def customer_delete(request, pk):
    """Delete a customer"""
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    customer.delete()
    return JsonResponse({'success': True})