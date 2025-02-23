from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Cart, Product, Category, Profile
from .square_service import client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
import json
import uuid
import shippo
from shippo.models import components

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


from django import template

register = template.Library()

def home(request):
    # Current date is hard coded
    date = "2024-12-06 17:00:00"
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

#login request
def login_user(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("YOU LOGGED IN"))
            return redirect('home')
        else:
            messages.success(request, ("ERROR TRY AGAIN"))
            return redirect('home')
#logout request
def logout_user(request):
    logout(request)
    messages.success(request, ("YOU LOGGED OUT"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        phone = request.POST.get("phone")
        text_messages = request.POST.get("text-checkbox") == "on"
        email_messages = request.POST.get("email-checkbox") == "on"

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.success(request, "Email is already in use. Try Logging in.")
            return redirect('home')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, f"Passwords do not match. Entered: {password} and {confirm_password}")
            return redirect('home')
          
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()

            # Get or create profile, then update phone number
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = phone  # Update phone field
            profile.text_messages = text_messages
            profile.email_messages = email_messages
            profile.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('home')
        except Exception as e:
            messages.success(request, f"Error creating account: {e}")
            return redirect('home')

    return redirect('home')

#shippo to create label (accept user address input)

shippo_sdk = shippo.Shippo(api_key_header="shippo_test_f3cb884569acedbe9a0860114d181ec57bed5277")
@csrf_exempt
def submit_address(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        print(f"Received data: {data}")

        address_from = components.AddressCreateRequest(
            name="MoonWalk Threads",
            company="",
            street1="490 High St",
            city="Auburn",
            state="CA",
            zip="95603",
            country="US",
            phone="(530) 401-1105",
            email="moonwalkthreads@gmail.com" #Need to get Lili's business email
        )

        address_to = components.AddressCreateRequest(
            name=data.get("customerFirstName") + " " + data.get("customerLastName"),
            company="",  # Optional; can be added if needed
            street1=data.get("customerStreetAddress"),
            street2=data.get("customerAddressOptional", ""),  # Optional address field
            city=data.get("customerCity"),
            state=data.get("customerState"),
            zip=data.get("customerZipCode"),
            country="US",
            phone=data.get("customerPhone"),
            email=data.get("customerEmail"),
        )

        print(f"Address from: {address_from}")
        print(f"Address to: {address_to}")

        parcel = components.ParcelCreateRequest(
            length="5",
            width="5",
            height="5",
            distance_unit=components.DistanceUnitEnum.IN,
            weight="2",
            mass_unit=components.WeightUnitEnum.LB
        )

        shipment = components.ShipmentCreateRequest(
            address_from=address_from,
            address_to=address_to,
            parcels=[parcel]
        )

        print(f"Shipment request: {shipment}")

        transaction = shippo_sdk.transactions.create(
            components.InstantTransactionCreateRequest(
                shipment=shipment,
                carrier_account="273e3a39e2884adc99f44020d3863b95", #Need Lili's shipping carrier acc for the API to work
                servicelevel_token="ontrac_ground" #Need Lili's info
            )
        )
        if transaction.status == "SUCCESS":
            return JsonResponse({
                'status': 'success',
                'tracking_number': transaction.tracking_number,
                'tracking_url': transaction.tracking_url,
                'label_url': transaction.label_url
            })
        else:
            error_message = ""

            if hasattr(transaction, 'messages'):
                try:
                    if isinstance(transaction.messages, list):
                        error_message = [str(msg) for msg in transaction.messages]
                    else:
                        error_message = str(transaction.messages)
                except Exception as e:
                    error_message = f"Error processing messages: {str(e)}"
            else:
                error_message = "Unknown error"

            return JsonResponse({
                'status': 'error',
                'message': error_message
            }, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@register.inclusion_tag('orderCartSummary.html', takes_context=True)
def orderCartSummary(context):
    return {
        'orderCartSummary': context['data'],
    }