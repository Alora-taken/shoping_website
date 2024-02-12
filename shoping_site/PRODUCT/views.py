from django.shortcuts import render

# Create your views here.
def brand(request):
    return render(request, 'PRODUCT/brands.html',context={}) 

def product(request):
    return render(request, 'PRODUCT/product.html',context={}) 

def product_filter(request):
    return render(request, 'PRODUCT/products_filters.html',context={}) 

def products(request):
    return render(request, 'PRODUCT/products.html',context={}) 