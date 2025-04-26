from django.contrib import admin
from .models import Category,Customer,Product,Order,OrderItem,Subscriber,Theme
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Subscriber)
admin.site.register(Theme)


#Mix customer info and user info
class CustomerInline(admin.StackedInline):
    model = Customer


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [CustomerInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_purchase']
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'square_order_id', 'total_amount', 'status', 'created_at']
    inlines = [OrderItemInline]

#unregister and re-register (django thing)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)