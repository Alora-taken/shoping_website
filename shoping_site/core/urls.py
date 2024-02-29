from django.urls import path
from .views import UserInfoAPIView, logout, UserProfileView, AddressListView, get_products, get_categories, filter_products

app_name='core'
urlpatterns = [
    path('api/user-info/', UserInfoAPIView.as_view(), name='user-info-api'),
    path('api/logout/', logout, name='api_logout'),
    path('get_products/', get_products, name='get_products'),
    path('filter_products/<int:category_id>/', filter_products, name='filter_products'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('addresses/', AddressListView.as_view(), name='user_addresses'),
    path('api/get_categories/', get_categories, name='get_categories'),
]

