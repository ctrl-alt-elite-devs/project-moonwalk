import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from django.urls import reverse
from storages.backends.s3boto3 import S3Boto3Storage
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

class Subscriber(models.Model):
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True)

    def get_unsubscribe_url(self):
        return reverse('unsubscribe', args=[str(self.unsubscribe_token)])
    
    def __str__(self):
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        return "Anonymous Subscriber"

# models.py

class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    banner_image =models.ImageField(storage=S3Boto3Storage(), upload_to='newsLetterBanner/')
    description = models.TextField()
    store_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    price= models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    size = models.CharField(max_length=20)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(storage=S3Boto3Storage(), upload_to='products/')
    featured = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    idempotency_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pre_tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivering = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, default='00000')
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_label_url = models.URLField(max_length=1000, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    square_order_id = models.CharField(max_length=100, unique=True, default='unknown')

    def __str__(self):
        if self.customer and self.customer.user:
            return f"Order #{self.id} - {self.customer.user.username}"
        return f"Order #{self.id} - Guest"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in Order #{self.order.id}"
    
class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Cart for {self.customer or self.session_key}'


class CheckoutInformation(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=10)

class Theme(models.Model):
    timeStamp = models.DateTimeField(auto_now=True, null=False, blank=False)
    backgroundColor = models.CharField(max_length=7, null=False, blank=False)
    dropDate = models.DateField()
    bannerImg00 = models.ImageField(storage=S3Boto3Storage(), upload_to='theme_img00/', null=False, blank=False)
    bannerImg01 = models.ImageField(storage=S3Boto3Storage(), upload_to='theme_img01/', null=False, blank=False)
    bannerImg02 = models.ImageField(storage=S3Boto3Storage(), upload_to='theme_img02/', null=False, blank=False)
    fontStyle = models.CharField(max_length=100, null=False, blank=False)
    dropTitle = models.CharField(max_length=30, null=False, blank=False)
    fontColor = models.CharField(max_length=7, null=False, blank=False)
    fontWeight = models.CharField(max_length=6, null=False, blank=False)
    fontBorderThickness = models.DecimalField(default=0, decimal_places=2, max_digits=3, null=False, blank=False)
    borderColor = models.CharField(max_length=7, null=False, blank=False)

    def __str__(self):
        return self.dropTitle
