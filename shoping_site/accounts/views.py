from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html',context={})

def profile(request):
    return render(request, 'profile.html', context={})

def sign_up(request):
    return render(request, 'signup.html', context={})