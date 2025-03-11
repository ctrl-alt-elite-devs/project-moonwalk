import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import datetime

# Create your models here.

#Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    text_messages = models.BooleanField(default = False)
    email_messages = models.BooleanField(default = False)

    # Address fields
    street_address = models.CharField(max_length=255, blank=True)
    street_address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
 
 
    def __str__(self):
        return self.user.username
     
    def create_customer(sender, instance, created, **kwargs):
        if created:
            user_customer = Customer(user=instance)
            user_customer.save()
    
    post_save.connect(create_customer, sender=User)
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price= models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    size = models.CharField(max_length=20)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    zipCode = models.CharField(max_length=10, default='00000')
    city = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='', blank=True)
    delivering = models.BooleanField(default = False)
    idempotency_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.customer}"
    
class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.customer or self.session_key}'


class CheckoutInformation(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=10)

