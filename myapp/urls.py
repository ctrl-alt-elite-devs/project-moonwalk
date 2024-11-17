from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.total_time, name='total_time'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('cart/',views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('googleCalendar/', views.googleCalendar, name='googleCalendar'),
    path('listLocations/', views.listLocations, name='listLocations'),

    #following path is just to test payment portal
    #must link to checkout process and delete this path
    path('payment/', views.paymentPortal, name='paymentPortal'),
]
