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
        fields = ['id', 'name', 'customer', 'city', 'state', 'details', 'postal_code', 'phone']
        read_only_fields = ['customer']
    def validate(self, attrs):
        user_token = self.context['request'].COOKIES.get('login_token')
        user = CustomUser.objects.get(token=user_token)
        attrs['customer'] = user
        return super().validate(attrs)