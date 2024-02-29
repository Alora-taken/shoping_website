from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_updated_by')
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_deleted_by')
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='customer', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    token = models.CharField(null=True, blank=True, max_length=1000)
    role = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('admin', 'Admin'), ('product_manager', 'Product Manager'), ('supervisor', 'Supervisor'), ('operator', 'Operator')], default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_image = models.ImageField(upload_to='profiles/', null=True, default='assets/img/transparent-photo-icon-for-your-interface-icon-picture-icon-5f9e5dcf942c94.2750417916042142236069copy.png')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
    
class Address(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    details = models.TextField()
    postal_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

class ProductCategory(BaseModel):
    name = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True,)
    product_image = models.ImageField(upload_to='category/', null=True, default='static/assets/img/transparent-photo-icon-for-your-interface-icon-picture-icon-5f9e5dcf942c94.2750417916042142236069copy.png')
    is_sub_cat = models.BooleanField(default=False)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    def __str__(self):
        return f"{self.name}"

class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    product_image = models.ImageField(upload_to='products/', null=True, default='static/assets/img/transparent-photo-icon-for-your-interface-icon-picture-icon-5f9e5dcf942c94.2750417916042142236069copy.png')
    stock_quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(ProductCategory, related_name='products')

class Discount(BaseModel):
    DISCOUNT_TYPES = [('percentage', 'Percentage'), ('amount', 'Amount')]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.FloatField()
    
    def __str__(self):
        return f"{self.get_discount_type_display()} - {self.value}"

class DiscountCode(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    expiration = models.DateTimeField(null = True)
    quantity = models.IntegerField(null = True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

class Order(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField()
    address = models.TextField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_finalized = models.BooleanField(default=False)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
