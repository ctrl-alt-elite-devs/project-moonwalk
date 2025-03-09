from django.contrib import admin
from .models import Category,Customer,Product,Order
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

#Mix customer info and user info
class CustomerInline(admin.StackedInline):
    model = Customer
 
 
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [CustomerInline]
 
#unregister and re-register (django thing)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)