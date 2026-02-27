from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Product
import json

@login_required
def product_list(request):
    """List all products"""
    products = Product.objects.filter(user=request.user)
    return render(request, 'products/product_list.html', {'products': products})

@login_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            mrp = request.POST.get('mrp')
            retail_price = request.POST.get('retail_price')
            manufacture_date = request.POST.get('manufacture_date')
            gst_rate = request.POST.get('gst_rate', 5.00)
            
            # Validate required fields
            if not all([name, mrp, retail_price, manufacture_date]):
                messages.error(request, 'Missing required fields. Please fill Name, MRP, Retail Price and Manufacture Date.')
                return redirect('product_create')  # ← changed: redirect back with error
            
            product = Product.objects.create(
                user=request.user,
                name=name,
                mrp=mrp,
                retail_price=retail_price,
                manufacture_date=manufacture_date,
                gst_rate=gst_rate
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()
            
            messages.success(request, f'Product "{product.name}" was added successfully!')
            return redirect('product_list')  # ← changed: redirect to list instead of JsonResponse
            
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
            return redirect('product_create')  # ← changed: redirect back with error
    
    return render(request, 'products/product_form.html')

@login_required
@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    """Edit a product"""
    product = get_object_or_404(Product, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name', product.name)
            product.mrp = request.POST.get('mrp', product.mrp)
            product.retail_price = request.POST.get('retail_price', product.retail_price)
            product.manufacture_date = request.POST.get('manufacture_date', product.manufacture_date)
            product.gst_rate = request.POST.get('gst_rate', product.gst_rate)
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            
            messages.success(request, f'Product "{product.name}" was updated successfully!')
            return redirect('product_list')  # ← changed: redirect to list
            
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
            return redirect('product_edit', pk=pk)  # ← changed: redirect back with error
    
    context = {'product': product}
    return render(request, 'products/product_form.html', context)

@login_required
@require_http_methods(["POST"])
def product_delete(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk, user=request.user)
    product_name = product.name  # save name before delete
    product.delete()
    
    messages.success(request, f'Product "{product_name}" was deleted successfully!')
    return redirect('product_list')  # ← changed: redirect to list instead of JsonResponse