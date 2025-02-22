from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Cart, Customer, Product, Category
from .square_service import client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from .models import Subscriber
import json
import uuid
import shippo
from shippo.models import components
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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

    search_query = request.GET.get('q', '').strip()

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

    if search_query:
        products = products.filter(name__icontains=search_query)

    categories = Category.objects.all()  # Pass all categories to the template
    return render(request, 'shop.html', {
        'products': products,
        'category': category,
        'categories': categories,
        'search_query': search_query,
        })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def cart(request):
    #mock items
        # Current date is hard coded
    date = "2025-02-06 00:00:00"
    today = datetime.datetime.now()
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = countdown_date - today
    # Convert the total time to seconds
    total_time = total_time.total_seconds()

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)

    # Render the cart page with items and total and timer count down
    return render(request, 'cart.html', {'total_time': total_time,'cart_items': cart_items,
        'total_price': total_price})

def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)

            # Ensure session key exists for non-logged-in users
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()

            # Determine whether to store by customer or session
            if request.user.is_authenticated:
                cart_item, created = Cart.objects.get_or_create(
                    product=product,
                    customer = Customer.objects.filter(user=request.user).first()
                )
            else:
                session_key = request.session.session_key
                cart_item, created = Cart.objects.get_or_create(
                    product=product,
                    session_key=session_key
                )

            # Determine message based on whether the item was newly added
            if created:
                message = "Item added to cart successfully."
            else:
                message = "Item is already in your cart."

            # Get updated cart count and total price
            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
            else:
                cart_items = Cart.objects.filter(session_key=session_key)

            cart_item_count = cart_items.count()
            total_price = sum(item.product.price for item in cart_items)

            print(f"Updated cart count: {cart_item_count}")

            return JsonResponse({
                'message': message,  # Updated message
                'cart_item_count': cart_item_count,
                'total_price': total_price,
            })

        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def remove_from_cart(request, cart_item_id):
    if request.method == "POST":
        try:
            cart_item = Cart.objects.get(id=cart_item_id)

            # Check if the item belongs to the current user/session
            if request.user.is_authenticated:
                if cart_item.customer == Customer.objects.filter(user=request.user).first():
                    cart_item.delete()
            else:
                if cart_item.session_key == request.session.session_key:
                    cart_item.delete()

            # Calculate updated cart item count and total price
            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
            else:
                session_key = request.session.session_key
                cart_items = Cart.objects.filter(session_key=session_key)

            cart_item_count = cart_items.count()
            total_price = sum(item.product.price for item in cart_items)
            print(f"Updated total price: {total_price}")

            return JsonResponse({
                'message': 'Item removed successfully.',
                'cart_item_count': cart_item_count,
                'total_price': total_price,
            })

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Item not found.'}, status=404)
        

    return JsonResponse({'message': 'Invalid request method.'}, status=400)
    



def merge_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    session_cart = Cart.objects.filter(session_key=session_key)
    customer_cart = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())

    for item in session_cart:
        cart_item, created = Cart.objects.get_or_create(
            customer = Customer.objects.filter(user=request.user).first(), product=item.product,
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
            print(result.body)
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
        idem_key = uuid.uuid4()

        #getting an uuid (for idempotency) (every payment needs one)

        try:
            result = client.payments.create_payment(
                body = {
                    "source_id": token,
                    "idempotency_key": str(idem_key),
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("YOU LOGGED IN"))
            return redirect('home')
        else:
            messages.success(request, ("ERROR TRY AGAIN"))
            return redirect('home')
    else:
        return render(request, 'login.html', {})
#logout request
def logout_user(request):
    logout(request)
    messages.success(request, ("YOU LOGGED OUT"))
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
    

@csrf_exempt  # Only use this for local testing, remove it if using CSRF middleware
def subscribe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"success": False, "message": "Invalid email address."}, status=400)

            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if not created:
                return JsonResponse({"success": False, "message": "You are already subscribed."})

            # Render HTML Email Content
            html_content = render_to_string("subscription.html", {"email": email})
            text_content = strip_tags(html_content)  # Convert HTML to plain text

            # Create Email with HTML and Plain Text
            subject = "🎉 Welcome to MoonWalk Threads!"
            from_email = "info@yourdomain.com"
            recipient_list = [email]

            email_message = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return JsonResponse({"success": True, "message": "Subscription successful."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid data format."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request."}, status=405)