from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Cart, Customer, Product, Category
from .square_service import client
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
import json
import uuid
import shippo
from shippo.models import components
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from square.client import Client
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .decorator import authenticated_user
from .decorator import checkout_required
from .decorator import payment_required



from django import template

register = template.Library()

client = Client(
    access_token='EAAAl0SURxUVKdImTqVNcvdSXqEg2AkVROJnO5TplGkliAUkGAwOkqTkqyBrUvG8',
    environment='sandbox'
)

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
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount

    # Render the cart page with items and total and timer count down
    return render(request, 'cart.html', {'total_time': total_time,'cart_items': cart_items,
        'total_price': total_price, 'tax_amount': tax_amount, 'tax_total': tax_total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
        cart_items = Cart.objects.filter(customer=customer)  # Only count current user's cart
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_item, created = Cart.objects.get_or_create(session_key=request.session.session_key, product=product)
        cart_items = Cart.objects.filter(session_key=request.session.session_key)  # Only count session cart

    if not created:
        return JsonResponse({
            'message': 'Product is already in the cart!',
            'cart_item_count': cart_items.count(),  # Fix: Count only the user's/session cart items
            'cart_items': []
        }, status=400)

    cart_item.save()

    # Fetch the latest cart items
    cart_items_data = [
        {
            "product": {
                "image_url": item.product.image.url if item.product.image else "",
                "name": item.product.name,
                "price": float(item.product.price),
            }
        }
        for item in cart_items[:4]  # Limit to first 4 for mini cart
    ]

    print("📦 Updated Cart Count:", cart_items.count())  # Debugging

    return JsonResponse({
        'message': 'Product added to cart successfully!',
        'cart_item_count': cart_items.count(),  # Fix: Return correct count
        'cart_items': cart_items_data
    })



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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount

    context = {
        'tax_amount': tax_amount,
        'tax_total': tax_total
    }
    return render(request, 'checkout.html', context)

def process_checkout(request):
    return

def store_order_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer=request.user.customer)
    else:
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key)

    request.session['checkout_data'] = {
        'email': request.POST.get('email'),
        'phone': request.POST.get('phone'),
        'address': request.POST.get('address') if 'address' in request.POST else None,
    }

    order_id, total_amount = create_square_order(cart_items)

    if order_id:
        request.session["order_id"] = order_id
        request.session["total_amount"] = total_amount
        return paymentPortal(request)
    else:
        return HttpResponse("Failed tp create order")

def create_order(request):
    if 'checkout_data' not in request.session or 'cart' not in request.session:
        print('checkout unsuccessful')
        return redirect('cart.html')

    checkout_data = request.session['checkout_data']
    cart_data = request.session['cart_data']

    print("checkout successful")
    return render(request, 'payment.html')

@authenticated_user
@payment_required
def orderSummary(request):
    send_order_email(request)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount
    return render(request, 'orderSummary.html',{'tax_amount': tax_amount, 'tax_total': tax_total})

# Creating the request for product details
def productDetails(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'productDetails.html', {'product': product})

@authenticated_user
@checkout_required
def paymentPortal(request):
    request.session['from_checkout'] = True
    
    square_app_id = 'sandbox-sq0idb-8IPgsCCDGo1xxuoCMh0SSQ'
    square_location_id = 'LNG128XEAPR21'

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount

    context = {
        "square_app_id": square_app_id,
        "square_location_id": square_location_id,
        'tax_amount': tax_amount,
        'tax_total': tax_total
    }

    return render(request, 'payment.html', context)

def create_square_order(cart_items):
    line_items = []

    for item in cart_items:
        line_item = {
            "name": str(item.product.name),
            "quantity": "1",
            "base_price_money": {
                "amount": int(item.product.price * 100),
                "currency": "USD"
            }
        }
        line_items.append(line_item)

    order_payload = {
        "order": {
            "location_id": "LNG128XEAPR21",
            "line_items": line_items,
            "taxes": [
                {
                    "uid": "STATE_SALES_TAX_UID",
                    "type": "ADDITIVE",
                    "scope": "ORDER",
                    "name": "Sales Tax",
                    "percentage": "7.25"
                }
            ],
            "pricing_options": {
                "auto_apply_taxes" : True
            }
        },
        "idempotency_key": str(uuid.uuid4())
    }

    result = client.orders.create_order(body=order_payload)

    if result.is_success():
        order = result.body["order"]
        order_id = order["id"]
        total_amount = order["total_money"]["amount"]

        return order_id, total_amount
    else:
        print(result.errors)
        return None, None

def process_payment(request):
    if request.method == 'POST':
        if not request.session.session_key:
                request.session.create()
        #get cart_items
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(customer=request.user.customer)
        else:
            session_key = request.session.session_key
            cart_items = Cart.objects.filter(session_key=session_key)

        #getting full amount calculated
        order_items = []
        total_price = 0
        for item in cart_items:
            order_items.append(f"{item.product.name}")
            total_price += item.product.price

        data = json.loads(request.body)
        customer_email = data.get("email", "guest@moonwalkthreads.com")
        user_first_name = request.user.first_name if request.user.is_authenticated else 'Guest'
        token = data.get("token")
        order_id = request.session.get("order_id")
        total_amount = request.session.get("total_amount")

        #getting an uuid (for idempotency) (every payment needs one)

        try:
            result = client.payments.create_payment(
                body = {
                    "source_id": token,
                    "idempotency_key": order_id,
                    "amount_money": {
                        "amount": total_amount,
                        "currency": "USD"
                    },
                    "autocomplete": True,
                    "order_id": order_id,
                    #"note": "Brief description"
                })
            if result.is_success:
                #return redirect('orderSummary.html')
                return JsonResponse({"status": "success", "payment_id}": result.body['payment']['id']})
            else:
                return JsonResponse({"status": "error", "errors": result.errors})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

@authenticated_user
def checkout(request):
    request.session['from_checkout'] = True
    return render(request, 'checkout.html', {}) 

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
    else:
        return render(request, 'login.html', {})   
#logout request
def logout_user(request):
    logout(request)
    messages.success(request, ("YOU LOGGED OUT"))
    return redirect('home')

#register user account
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
            messages.success(request, f"Passwords do not match. Entered: {password} and {confirm_password}")
            return redirect('home')
          
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()

            # Get or create customer, then update phone number
            customer, created = Customer.objects.get_or_create(user=user)
            customer.phone = phone  # Update phone field
            customer.text_messages = text_messages
            customer.email_messages = email_messages
            customer.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
        except Exception as e:
            messages.success(request, f"Error creating account: {e}")
            return redirect('home')

    return redirect('home')

class password_reset(FormView):
    form_class = PasswordResetForm  # Built-in Django form

    def form_valid(self, form):
        form.save(
            use_https=self.request.is_secure(),
            request=self.request,
            email_template_name="registration/password_reset_email.txt",       # plain text fallback
            html_email_template_name="registration/password_reset_email.html", 
        )
        return JsonResponse({"success": True}) # Return JSON response to be checked in login-script

#shippo to create label (accept user address input)

shippo_sdk = shippo.Shippo(api_key_header="shippo_test_f3cb884569acedbe9a0860114d181ec57bed5277")
@csrf_exempt
def submit_address(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        '''data = json.loads(request.body)
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
            }, status=400)'''

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@register.inclusion_tag('orderCartSummary.html', takes_context=True)
def orderCartSummary(context):
    return {
        'orderCartSummary': context['data'],
    }


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

def send_order_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_email = data.get("email", "guest@moonwalkthreads.com")  # Default for guests
            user_first_name = request.user.first_name if request.user.is_authenticated else "Guest"

            # Fetch cart items for the user (or guest session)
            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(customer=request.user.customer)
            else:
                session_key = request.session.session_key
                cart_items = Cart.objects.filter(session_key=session_key)

            # Format order details
            order_items = []
            total_price = 0
            for item in cart_items:
                order_items.append(f"{item.product.name} - ${item.product.price}")
                total_price += item.product.price

            # Render the email template
            html_content = render_to_string("order_confirmation_email.html", {
                "first_name": user_first_name,
                "email": customer_email,
                "order_items": order_items,
                "total_price": total_price,
            })
            text_content = strip_tags(html_content)

            # Send email
            subject = "🛍️ Your MoonWalk Threads Order Confirmation"
            from_email = "orders@moonwalkthreads.com"
            recipient_list = [customer_email]

            email_message = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return orderSummary(request)
            return JsonResponse({"success": True, "message": "Order confirmation email sent."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid data format."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request."}, status=405)

@login_required
def profile(request):
    # Check if a user is logged in
    if request.user.is_authenticated:
        user_data = {
            "email": request.user.email,
            "password": "********",  # Hidden for security
            "address": request.user.customer.street_address if hasattr(request.user, "customer") else "No address available",
            "orders": [],  # Placeholder for future order retrieval
        }
    else:
        # Hardcoded data for non-logged-in users
        user_data = {
            "email": "guest@example.com",
            "password": "********",
            "address": "No address available",
            "orders": [
                {"id": 1, "status": "Shipped", "total": 59.99},
                {"id": 2, "status": "Processing", "total": 120.50},
            ],
        }

    return render(request, "profile.html", {"user_data": user_data})

