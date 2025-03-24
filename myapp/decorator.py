from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

# check if user is logged in or not
# if user is logged in, may access checkout page
# if user is NOT logged in, may NOT access checkout page
def authenticated_user(view_func): # view_func is the function being passed to this decorator
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs) # if user is authenticated, redirect them to the view_function
        else:
            messages.error(request, "You need to log in to checkout.")
            return redirect('home') # if user is NOT authenticated, redirect them to home
    return wrapper_func

# check if user came from checkout page before being allowed into payment page.
# if did come from checkout can proceed.
# if did NOT come from checkout, redirect to checkout page.
def checkout_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('from_checkout'): # if NOT at checkout previously
            return redirect('checkout') # redirect to checkout
        request.session.pop('from_checkout', None)
        return view_func(request, *args, **kwargs)
    return wrapper_func

# check if user came from payment page before being allowed into order summary page.
# if did come from payment can proceed.
# if did NOT come from payment, redirect to checkout page.
def payment_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if not request.session.get('from_paymentPortal'): 
            return redirect('checkout')
        request.session.pop('from_paymentPortal', None)
        return view_func(request, *args, **kwargs)
    return wrapper_func