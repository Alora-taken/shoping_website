from django.urls import path
from .views import UserInfoAPIView, logout, UserProfileView, AddressListView

app_name='core'
urlpatterns = [
    path('api/user-info/', UserInfoAPIView.as_view(), name='user-info-api'),
    path('api/logout/', logout, name='api_logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('addresses/', AddressListView.as_view(), name='user_addresses'),
]

