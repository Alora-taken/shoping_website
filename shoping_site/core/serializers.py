from rest_framework import serializers
from .models import CustomUser, Address, Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'info']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'user_image']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name','customer.id', 'city', 'state', 'details', 'postal_code', 'phone']