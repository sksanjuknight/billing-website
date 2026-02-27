from decimal import Decimal
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
from .models import Invoice, InvoiceItem
from apps.products.models import Product
from apps.customers.models import Customer
from apps.expenses.models import Expense
import json
from urllib.parse import quote   # ← NEW (for WhatsApp)
from apps.core.models import BusinessProfile


# Dashboard view
@login_required
def dashboard(request):
    invoices = Invoice.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_sales = invoices.aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    profit = total_sales - total_expenses

    payments_received = invoices.aggregate(
        total_paid=Sum('amount_paid')
    )['total_paid'] or Decimal('0.00')

    today = timezone.now().date()
    first_of_month = today.replace(day=1)
    month_invoices = invoices.filter(invoice_date__gte=first_of_month)
    month_sales = month_invoices.aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')
    month_expenses = expenses.filter(date__gte=first_of_month).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    month_profit = month_sales - month_expenses

    recent_invoices = invoices.order_by('-invoice_date')[:5]

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'payments_received': payments_received,
        'month_sales': month_sales,
        'month_expenses': month_expenses,
        'month_profit': month_profit,
        'recent_invoices': recent_invoices,
    }

    return render(request, 'dashboard.html', context)


def generate_invoice_number(user):
    today = timezone.now().date()
    prefix = f"INV-{today.strftime('%Y%m%d')}"
    count = Invoice.objects.filter(user=user, invoice_number__startswith=prefix).count()
    return f"{prefix}-{count + 1:04d}"


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


@login_required
@require_http_methods(["GET", "POST"])
def invoice_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer = get_object_or_404(Customer, id=data['customer'], user=request.user)

            invoice = Invoice.objects.create(
                user=request.user,
                customer=customer,
                invoice_number=generate_invoice_number(request.user),
                invoice_date=datetime.strptime(data['invoice_date'], '%Y-%m-%d').date(),
                due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
                amount_paid=Decimal(str(data.get('amount_paid', '0.00'))),
                status='draft'
            )

            for item in data.get('items', []):
                product = get_object_or_404(Product, id=item['product_id'], user=request.user)
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=int(item['quantity']),
                    price_per_unit=Decimal(item['price_per_unit']),
                    gst_rate=Decimal(item.get('gst_rate', product.gst_rate or 0))
                )

            invoice.calculate_totals()
            invoice.update_status_from_payments()

            return JsonResponse({
                'success': True,
                'invoice_id': invoice.id,
                'invoice_number': invoice.invoice_number
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    products = Product.objects.filter(user=request.user, is_active=True)
    customers = Customer.objects.filter(user=request.user)
    return render(request, 'billing/invoice_form.html', {
        'products': products,
        'customers': customers,
    })


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)

    # Business profile (your company)
    business = BusinessProfile.objects.get(user=request.user)

    # Customer
    customer = invoice.customer
    phone = customer.phone if customer else ""

    # Dynamic invoice URL (works on localhost & production)
    invoice_url = request.build_absolute_uri(
        f"/billing/{invoice.id}/pdf/"
    )

    # WhatsApp message template
    message = f"""
Dear {customer.name},

Greetings from {business.business_name}.

Invoice No: {invoice.invoice_number}
Amount Due: ₹{invoice.balance_due}

Please find the invoice here:
{invoice_url}

Thank you,
{business.business_name}
{business.contact_details}
"""

    # Final WhatsApp link
    whatsapp_url = f"https://wa.me/{business.whatsapp_number}?text={quote(message)}"

    return render(request, "billing/invoice_detail.html", {
        "invoice": invoice,
        "whatsapp_url": whatsapp_url
    })


@login_required
@require_http_methods(["POST"])
def invoice_update_status(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    data = json.loads(request.body)
    invoice.status = data.get('status', invoice.status)
    invoice.save()
    return JsonResponse({'success': True})


@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    return render(request, 'billing/invoice_pdf.html', {'invoice': invoice})


@login_required
@require_http_methods(["POST"])
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    invoice.delete()
    return JsonResponse({'success': True})


# ------------------ PAYMENTS ------------------

@require_POST
@login_required
def invoice_add_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    amount = Decimal(request.POST.get('amount', '0'))

    invoice.amount_paid += amount
    invoice.update_status_from_payments()

    return redirect('billing:invoice_detail', pk=pk)


@require_POST
@login_required
def invoice_mark_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    invoice.amount_paid = invoice.grand_total
    invoice.update_status_from_payments()

    return redirect('billing:invoice_detail', pk=pk)
