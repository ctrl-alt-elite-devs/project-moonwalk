from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Cart, Customer, Product, Category, Subscriber
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
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re



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

def store_order_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer=request.user.customer)
    else:
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key)

    if request.method == "POST":
        data = json.loads(request.body)
    else:
        return HttpResponse("Failed tp create order")

    '''customerInfo = {
        'first_name': data.get("customerFirstName"),
        'last_name': data.get('customerLastName'),
        'email': data.get('customerEmail'),
        'phone': data.get('customerPhone'),
        'address': data.get('address', None),
    }'''

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

#@authenticated_user
@payment_required
def orderSummary(request):
    #send_order_email(request)
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

#@authenticated_user
@checkout_required
def paymentPortal(request):
    request.session['from_paymentPortal'] = True
    
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

def create_square_customer(customerInfo):
    id = str(uuid.uuid4())

    if customerInfo["delivery_method"] == "Pickup":
        address_details = {}
    else:
        address_details = {
            "address_line_1": customerInfo["address"]["streetAddress"],
            "address_line_2": customerInfo["address"]["addressOptional"],
            "administrative_district_level_1": customerInfo["address"]["state"],
            "country": "US",
            "locality": customerInfo["address"]["city"],
            "postal_code": customerInfo["address"]["zipCode"],
        }

    result = client.customers.create_customer(
    body = {
        "idempotency_key": id,
        "given_name": customerInfo["first_name"],
        "family_name": customerInfo["last_name"],
        "email_address": customerInfo["email"],
        "phone_number": customerInfo["phone"],
        "address" : {
            "address_line_1": customerInfo["address"]["streetAddress"],
            "address_line_2": customerInfo["address"]["addressOptional"],
            "administrative_district_level_1": customerInfo["address"]["state"],
            "country": "US",
            "locality": customerInfo["address"]["city"],
            "postal_code": customerInfo["address"]["zipCode"],
        }
    })

    customer = result.body["customer"]
    customer_id = customer["id"]

    if result.is_success():
        return customer_id
    elif result.is_error():
        return None

def create_square_order(cart_items, customerInfo, delivery_method):
    #create customer to associate with order
    customer_id = create_square_customer(customerInfo)

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

    if delivery_method == "Pickup":
        fulfillments = [
            {
                "type": "PICKUP",
                "state": "PROPOSED",
                "pickup_details": {
                    "recipient": {
                        "customer_id": customer_id
                    },
                    "schedule_type": "ASAP"
                }
            }
        ]
    else:
        fulfillments = [
                    {
                        "type": "SHIPMENT",
                        "state": "PROPOSED",
                        "shipment_details": {
                            "recipient": {
                                "customer_id": customer_id
                            },
                            "schedule_type": "ASAP"
                        }
                    }
                ]

    order_payload = {
        "order": {
            "location_id": "LNG128XEAPR21",
            "customer_id": customer_id,
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
            },
            "fulfillments": fulfillments
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
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get("token")
        delivery_method = data.get("delivery_method")
        customer_email = data.get("email")
        customer_first_name = data.get("first_name")
        customer_last_name = data.get("last_name")
        customer_phone = data.get("phone")
        customer_address = data.get("address")

        customerInfo = {
            "first_name": customer_first_name,
            "last_name": customer_last_name,
            "email": customer_email,
            "phone": customer_phone,
            "address": customer_address,
            "delivery_method": delivery_method
        }


        # 🛒 Retrieve Cart Items
        if request.user.is_authenticated:
            customer = request.user.customer
            cart_queryset = Cart.objects.filter(customer=customer)
        else:
            session_key = request.session.session_key
            cart_queryset = Cart.objects.filter(session_key=session_key)

        # Ensure cart is not empty
        if not cart_queryset.exists():
            return JsonResponse({"status": "error", "message": "Cart is empty"}, status=400)

        # **Step 1: Create Order in Square**
        square_order_id, total_amount = create_square_order(cart_queryset, customerInfo, delivery_method)

        if not square_order_id:
            return JsonResponse({"status": "error", "message": "Failed to create Square order"}, status=505)

        # **Step 2: Process Payment Using Square Order ID**
        payment_request = {
            "source_id": token,
            "idempotency_key": str(uuid.uuid4()),  # Generate unique key
            "amount_money": {
                "amount": total_amount,
                "currency": "USD"
            },
            "autocomplete": True,
            "order_id": square_order_id  # ✅ Use Square's Order ID
        }

        payment_result = client.payments.create_payment(body=payment_request)

        if payment_result.is_success():
            # ✅ Payment Successful, Send Confirmation Email
            square_order_id = payment_result.body['payment']['order_id']  # or wherever the order ID is

            email_context = {
                **customerInfo,  # expands: first_name, last_name, email, phone, address
                "delivery_method": delivery_method.lower(),
                "address_details": customerInfo["address"] if delivery_method.lower() == "delivery" else {},
                "order_items": [
                    {
                        "name": item.product.name,
                        "price": item.product.price,
                        "image_url": item.product.image.url if item.product.image else ""
                    } for item in cart_queryset
                ],
                "total_price": total_amount / 100,  # cents to dollars
                "square_order_id": square_order_id,  # ✅ ADD THIS
            }

            send_order_email(email_context)

            return JsonResponse({"status": "success", "message": "Payment successful!","square_order_id": square_order_id})

        else:
            return JsonResponse({"status": "error", "message": payment_result.errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=501)

#@authenticated_user
def checkout(request):
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

    return render(request, 'checkout.html', context)

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
            context = {"login_error": "Incorrect email or password"}
            return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', {})   
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

        errors = {}

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            errors["email_error"] = "Please enter a valid email address."

        # Check that passwords match and that password is strong enough
        if password != confirm_password:
            errors["password_match_error"] = "Passwords do not match."
        else:
            try:
                custom_password_validator(password)
            except ValidationError as e:
                errors["password_strength_error"] = " ".join(e.messages)

        # Validate phone number (example regex: 9 to 15 digits, optional +)
        phone_regex = r"^\+?1?\d{9,15}$"
        if phone and not re.match(phone_regex, phone):
            errors["phone_error"] = "Please enter a valid phone number (9-15 digits, may include country code)."

        # Check if email is already registered
        if User.objects.filter(username=username).exists():
            errors["username_error"] = "Email is already in use. Try logging in."

        if errors:
            # Re-render the home page (or the signup page) with the errors in the context.
            context = {
                "signup_errors": errors,
                "signup_data": {
                    "email": request.POST.get("email"),
                    "first_name": request.POST.get("first-name"),
                    "last_name": request.POST.get("last-name"),
                    "phone": request.POST.get("phone"),
                    "text_checkbox": request.POST.get("text-checkbox"),
                    "email_checkbox": request.POST.get("email-checkbox"),
                }
            }
            return render(request, 'home.html', context)

        try:
            user = User.objects.create_user(username=username, password=password, email=email,
                                            first_name=first_name, last_name=last_name)
            user.save()

            # Create or update customer info
            customer, created = Customer.objects.get_or_create(user=user)
            customer.phone = phone
            customer.save()

            if email_messages:
                Subscriber.objects.get_or_create(email=email)

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
        except Exception as e:
            errors["server_error"] = f"Error creating account: {e}"
            context = {"signup_errors": errors}
            return render(request, 'home.html', context)
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

def custom_password_validator(password):
    # Check for a minimum length of 8 characters
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    # Check for at least one uppercase letter
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    
    # Check for at least one lowercase letter
    if not any(c.islower() for c in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    # Check for at least one digit
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one number.")


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

# def send_order_email(context):
#     """Send order confirmation email to the customer with tax info."""

#     # Render email
#     html_content = render_to_string("order_confirmation_email.html", context)
#     text_content = strip_tags(html_content)

#     subject = f"Order #{context['square_order_id']}"
#     from_email = "projectmoonwalk01@gmail.com"
#     recipient_list = [context["email"]]

#     email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
#     email.attach_alternative(html_content, "text/html")
    
#     # ✉️ Commented out email sending for testing
#     # email.send()

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

