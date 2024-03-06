from django.contrib import admin
from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    
]