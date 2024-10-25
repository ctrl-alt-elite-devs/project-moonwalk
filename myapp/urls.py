from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('cart/',views.cart, name='cart') 
    path('contact/', views.contact, name='contact'),
    path('googleCalendar/', views.googleCalendar, name='googleCalendar'),
]
