from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('/products/')
    return render(request, 'products/confirm_delete.html', {'object': product, 'type': 'Product'})

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('/products/')
    return render(request, 'products/confirm_delete.html', {'object': category, 'type': 'Category'})
 