from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # path('', views.total_time, name='total_time'),
    
    # Shop and Filtering
    path('shop/<str:foo>/', views.shop, name='shop-category'),
    path('shop/', views.shop, name='shop'),

    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Google Calendar
    path('googleCalendar/', views.googleCalendar, name='googleCalendar'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/store_data', views.store_order_data, name='store_order_data'),
    path('checkout/payment/', views.paymentPortal, name='payment'),
    path('orderSummary/', views.orderSummary, name='orderSummary'),
    path('process_payment/', views.process_payment, name='process_payment'),

    # Product Details
    path('product/<int:pk>/', views.productDetails, name='productDetails'),

    # Address Submission (Shippo)
    path('submit-address/', views.submit_address, name='submit_address'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # Payment Portal (Testing)
    path('payment/', views.paymentPortal, name='paymentPortal'),

    # User Profile
    path('profile/', views.profile, name='profile')
]
