from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'CUSTOMERS/index.html',context={}) 

def contact(request):
    return render(request, 'CUSTOMERS/contacts.html',context={}) 
