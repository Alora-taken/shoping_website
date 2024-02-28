from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy
from import_export.admin import ImportExportActionModelAdmin
from .models import CustomUser, Address, ProductCategory, Product, Discount, DiscountCode, Order, OrderItem
from django.contrib.auth.models import Group
from admin_interface.models import Theme
from django.utils import timezone
from django.utils.html import format_html
from django.templatetags.static import static
    
        
class CustomAdminSite(AdminSite):
    site_header = 'فروشگاه آنلاین'  
    site_title = 'فروشگاه آنلاین'  
    index_title = 'پنل مدیریت فروشگاه'  

custom_admin_site = CustomAdminSite()
admin.site = custom_admin_site

class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'city', 'state', 'details', 'is_deleted_colored')
    search_fields = ('customer__email', 'city', 'state')
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'parent_category', 'is_deleted_colored')
    search_fields = ('name',)
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted','parent_category')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','price', 'description', 'stock_quantity', 'display_categories', 'is_deleted_colored')
    search_fields = ('name', 'categories__name')
    
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = 'Categories'
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()
    
class DiscountAdmin(ImportExportActionModelAdmin):
    list_display = ('discount_type', 'value', 'is_deleted_colored')
    search_fields = ('discount_type',)
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()
    
class DiscountCodeAdmin(ImportExportActionModelAdmin):
    list_display = ('code', 'expiration', 'quantity', 'discount', 'is_deleted_colored')
    search_fields = ('code', 'discount__discount_type')
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()
        
class OrderAdmin(ImportExportActionModelAdmin):
    list_display = ('customer', 'total_price', 'address', 'discount', 'is_finalized', 'is_deleted_colored')
    search_fields = ('customer__email', 'address')
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()
    
class OrderItemAdmin(ImportExportActionModelAdmin):
    list_display = ('order', 'product', 'quantity', 'is_deleted_colored')
    search_fields = ('order__customer__email', 'product__name')
    
    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background-color: red;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
        return format_html('<span style="background-color: green;border-radius:5px;padding:10px;">{}</span>', obj.is_deleted)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('is_deleted')
    
    is_deleted_colored.short_description = 'Is Deleted'
    is_deleted_colored.admin_order_field = 'is_deleted'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:  
            obj.created_by = request.user
        else:  
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
            if not obj.is_deleted:
                obj.deleted_by = None
                obj.deleted_at = None 
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        deleted_by = request.user
        deleted_at = timezone.now()

        obj.is_deleted = True
        obj.deleted_by = deleted_by
        obj.deleted_at = deleted_at
        obj.save()
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

# Register your models with the admin site
admin.site.register(Group, GroupAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(CustomUser)
admin.site.register(Address, AddressAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
