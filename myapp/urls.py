from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    # path('', views.total_time, name='total_time'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('cart/',views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('contact/', views.contact, name='contact'),
    path('googleCalendar/', views.googleCalendar, name='googleCalendar'),
    path('listLocations/', views.listLocations, name='listLocations'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:pk>', views.productDetails, name='productDetails'), # Product details page,
    path('orderSummary/', views.orderSummary, name='orderSummary'),
    path('checkout/payment.html', views.paymentPortal, name='payment'),
    path('shop/<str:foo>', views.shop, name='shop-category'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    #following path is just to test payment portal
    #must link to checkout process and delete this path
    path('payment/', views.paymentPortal, name='paymentPortal')

]
