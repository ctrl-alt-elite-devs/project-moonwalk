from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # path('', views.total_time, name='total_time'),
    
    # Admin CSS Editor
    path('edit-theme/', views.edit_theme, name='edit-theme'),
    path('submit_theme/', views.submit_theme, name='submit_theme'),
    
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
    path('order-summary/', views.orderSummary, name='orderSummary'),
    path("order-summary/<int:order_id>/", views.orderSummary, name="view_order_summary"),
    path('process_payment/', views.process_payment, name='process_payment'),

    # Product Details
    path('product/<int:pk>/', views.productDetails, name='productDetails'),
    
    #send order
    path("send-order-email/", views.send_order_email, name="send_order_email"),
    
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/<uuid:token>/", views.unsubscribe, name="unsubscribe"),

    # Address Submission (Shippo)
    path('get-shipping-rates/', views.get_shipping_rates, name='get_shipping_rates'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', views.password_reset.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', login_required(auth_views.PasswordChangeView.as_view()), name='password_change'),
    path('password_change/done/', login_required(auth_views.PasswordChangeDoneView.as_view()), name='password_change_done'),
    path('update-address/', views.update_address, name='update_address'),


    # Payment Portal (Testing)
    path('payment/', views.paymentPortal, name='paymentPortal'),

    # User Profile
    path('profile/', views.profile, name='profile')
]
