from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_roles

@login_required
@allowed_roles(roles=['admin','cashier'])
def product_list(request):
    print("HELLO !!!")
    products=Product.objects.all()
    return render(request,'inventory/product_list.html',{'products':products})

@login_required
@allowed_roles(roles=['admin'])
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('product_list')
    else:
        form = ProductForm()  # GET request, blank form
    return render(request, 'inventory/product_form.html', {'form': form})

@login_required
@allowed_roles(roles=['admin'])   
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
        # If POST is invalid, form will fall through to render with errors
    else:
        form = ProductForm(instance=product)  # GET request → pre-fill form

    # Always return an HttpResponse
    return render(request, 'inventory/product_form.html', {'form': form})

@login_required
@allowed_roles(roles=['admin'])
def product_delete(request,pk):
    product= get_object_or_404(Product,pk=pk)
    product.delete()
    messages.success(request,"Product deleted successfully.")
    return redirect('product_list')
