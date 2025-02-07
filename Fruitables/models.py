
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive','Inactive'),
)

class User(AbstractUser):
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    user_profile_image = models.ImageField(upload_to='user', null=True, blank=True)
    face_encoding = models.JSONField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(null=True,blank=True)
    image = models.ImageField(upload_to='product')
    slug = AutoSlugField(populate_from='title')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wished_item = models.ForeignKey(Product,on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='wished_item')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wished_item.title
 
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Shipped', 'Shipped'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.product.title} by {self.user.username}"

    def calculate_total(self):
        total = sum(item.total_price() for item in self.order_items.all())
        self.total_amount = total
        self.save()

    def total_price(self):
        return self.product.price * self.quantity    

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, related_name="shipping_address", on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp = models.DateTimeField(auto_now=True, editable=False)
    

    def _str_(self):
        return self.name