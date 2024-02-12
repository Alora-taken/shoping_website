from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Address(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    details = models.TextField()

class ProductCategory(BaseModel):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')

class Discount(BaseModel):
    DISCOUNT_TYPES = [('percentage', 'Percentage'), ('amount', 'Amount')]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.FloatField()

class DiscountCode(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

class Order(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_finalized = models.BooleanField(default=False)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()