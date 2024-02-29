from django.shortcuts import render

# Create your views here.
def brand(request):
    return render(request, 'PRODUCT/brands.html',context={}) 

def product(request):
    return render(request, 'PRODUCT/product.html',context={}) 

def product_filter(request, category_id):
    return render(request, 'PRODUCT/products_filters.html',context={'cat_id':category_id}) 

def products(request):
    return render(request, 'PRODUCT/products.html',context={}) 