from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"Image for {self.product.name}"

class PaymentSettings(models.Model):
    business_name = models.CharField(max_length=255)
    stripe_public_key = models.CharField(max_length=255)
    stripe_secret_key = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name

class SiteSettings(models.Model):
    shop_name = models.CharField(max_length=100, default="My Shop")
    products_name = models.CharField(max_length=100, default="Product List")

    def __str__(self):
        return "Site Settings"

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=100, default='Unknown')       # <-- Must exist
    last_name = models.CharField(max_length=100, default='Unknown')        # <-- Must exist
    street_address = models.CharField(max_length=255, default='Unknown')      # Example address field
    house_number = models.CharField(max_length=50, default='Unknown')         # Example house number
    postal_code = models.CharField(max_length=20, default='Unknown')        # <-- Must exist
    city = models.CharField(max_length=100, blank=True, null=True)    # ADD
    state = models.CharField(max_length=100, blank=True, null=True)   # ADD
    country = models.CharField(max_length=100, blank=True, null=True) # ADD
    
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
