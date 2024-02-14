from django.shortcuts import render

# Create your views here.
def order(request):
    return render(request, 'ORDERS/order.html',context={}) 

def orders(request):
    return render(request, 'ORDERS/orders.html',context={}) 

def shoping_cart(request):
    return render(request, 'ORDERS/shopping_cart.html',context={}) 