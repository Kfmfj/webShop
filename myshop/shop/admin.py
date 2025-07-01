from django.contrib import admin
from .models import Product, ProductImage, PaymentSettings, SiteSettings, Order, OrderItem


class ProductImageInline(admin.TabularInline): 
    model = ProductImage
    extra = 1  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(PaymentSettings)
admin.site.register(SiteSettings)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'first_name', 
        'last_name', 
        'email', 
        'postal_code', 
        'phone', 
        'city', 
        'state', 
        'country', 
        'stripe_payment_intent', 
        'created_at'
        ]
    ordering = ['-created_at']
    search_fields = [
        'first_name', 
        'last_name', 
        'email', 'phone', 
        'postal_code'
        ]
    list_filter = ['created_at']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    search_fields = ['product__name', 'order__id']
