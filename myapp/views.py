from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Cart, Product, Category
from .square_service import client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
import json
import uuid

def home(request):
    # Current date is hard coded
    date = "2025-04-10 17:00:00" # This is the actual date that changes the timer
    today = datetime.datetime.now()
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = countdown_date - today
    # Convert the total time to seconds
    total_time = total_time.total_seconds()
    products = Product.objects.all()
    featured = Product.objects.filter(featured=True)
    return render(request, 'home.html', {'total_time': total_time, 'products':products, 'featured':featured})
    # return render(request, 'home.html')


def total_time(request):
    # Current date is hard coded
    date = "2024-12-06 17:00:00"
    today = datetime.datetime.now
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = countdown_date - today
    # Convert the total time to seconds
    total_time = total_time.total_seconds()
    context = {
        'total_time': total_time
    }
    return render(request, 'home.html', 'cart.html', context)

def shop(request, foo=None):
    # If a category is provided (foo), filter by category, else show all products
    if foo:
        foo = foo.replace('-', ' ')
        try:
            category = Category.objects.get(name=foo)
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            messages.success(request, ("Category Doesn't Exist!"))
            return redirect('shop')
    else:
        # No category, show all products
        products = Product.objects.all()
        category = None  # No category selected

    categories = Category.objects.all()  # Pass all categories to the template
    return render(request, 'shop.html', {'products': products, 'category': category, 'categories': categories})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def cart(request):
    #mock items
        # Current date is hard coded
    date = "2024-12-06 00:00:00"
    today = datetime.datetime.now()
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = countdown_date - today
    # Convert the total time to seconds
    total_time = total_time.total_seconds()

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer=request.user.customer)
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)

    # Render the cart page with items and total and timer count down
    return render(request, 'cart.html', {'total_time': total_time,'cart_items': cart_items,
        'total_price': total_price})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_item, created = Cart.objects.get_or_create(session_key=request.session.session_key, product=product)

    # Handle if the product is already in the cart
    if not created:
        return JsonResponse({'message': 'Product is already in the cart!'}, status=400)

    cart_item.save()
    return JsonResponse({'message': 'Product added to cart successfully!'})

def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':  # Ensure the method is POST for safety
        cart_item = get_object_or_404(Cart, id=cart_item_id)

        # Check if the user is authorized to remove this item
        if request.user.is_authenticated:
            if cart_item.customer != request.user.customer:
                return JsonResponse({'message': 'Unauthorized access.'}, status=403)
        else:
            if cart_item.session_key != request.session.session_key:
                return JsonResponse({'message': 'Unauthorized access.'}, status=403)

        cart_item.delete()  # Remove the item from the cart
        return JsonResponse({'message': 'Item removed successfully!'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


def merge_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    session_cart = Cart.objects.filter(session_key=session_key)
    customer_cart = Cart.objects.filter(customer=user.customer)

    for item in session_cart:
        cart_item, created = Cart.objects.get_or_create(
            customer=user.customer, product=item.product,
        )
        if not created:
            cart_item.save()
        item.delete()

def googleCalendar(request):
    iframe_code = '''
    <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FLos_Angeles&showPrint=0&title=MoonWalk%20Threads%20Events&src=OTAwZmRmNjUwYjU3OWEwMDdmZWI2ZTdmOGFjODc5MTkwMzM3ZDAwZWFjOGU2MmFlZmZiYmI2Y2Q5ZmYxMGRmM0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23F09300" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>
    '''
    return render(request, 'googleCalendar.html', {'iframe_code': iframe_code})

@csrf_exempt
def checkout(request):
    return render(request, 'checkout.html')

def orderSummary(request):
    return render(request, 'orderSummary.html')

#testing square api's
def listLocations(request):
    if request.method == "GET":
        try:
            result = client.locations.list_locations()
            if result.is_success():
                locations = result.body['locations']
                return JsonResponse({"status": "success", "locations": locations})
            else:
                return JsonResponse({"status": "error", "errors": result.errors})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request number"})


# Creating the request for product details
def productDetails(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'productDetails.html', {'product': product})


def paymentPortal(request):
    square_app_id = 'sandbox-sq0idb-8IPgsCCDGo1xxuoCMh0SSQ'
    square_location_id = 'LNG128XEAPR21'
    context = {
        "square_app_id": square_app_id,
        "square_location_id": square_location_id
    }
    return render(request, 'payment.html', context)

def process_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get("token")
        amount = 100

        #getting an uuid (for idempotency) (every payment needs one)

        try:
            result = client.payments.create_payment(
                body = {
                    "source_id": token,
                    "idempotency_key": "7b0f3ec5-086a-4871-8f13-3c81b3875218",
                    "amount_money": {
                        "amount": amount,
                        "currency": "USD"
                    },
                    "autocomplete": True,
                    #"customer_id": "W92WH6P11H4Z77CTET0RNTGFW8",
                    "note": "Brief description"
                })
            if result.is_success:
                return JsonResponse({"status": "success", "payment_id}": result.body['payment']['id']})
            else:
                return JsonResponse({"status": "error", "errors": result.errors})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})