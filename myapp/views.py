from decimal import Decimal
from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from django.urls import reverse
from .models import Cart, Customer, Product, Category, Subscriber, Order, OrderItem, Theme
from .square_service import client
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
import re
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
from django.views.decorators.http import require_POST
import re



from django import template

register = template.Library()
shippo_sdk = shippo.Shippo(api_key_header="shippo_test_f3cb884569acedbe9a0860114d181ec57bed5277")
client = Client(
    access_token='EAAAl0SURxUVKdImTqVNcvdSXqEg2AkVROJnO5TplGkliAUkGAwOkqTkqyBrUvG8',
    environment='sandbox'
)

def home(request):
    # Current date is hard coded
    latest_entry = Theme.objects.latest('timeStamp')
    date = datetime.datetime.strptime(str(latest_entry.dropDate), "%Y-%m-%d")
    today = datetime.datetime.now()
    timestamp_date = date.timestamp()
    timestamp_today = today.timestamp()
    # Specify the date format being provided
    #countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = timestamp_date - timestamp_today
    print(total_time)
    # Convert the total time to seconds
    featured = Product.objects.filter(featured=True,  quantity__gt=0)
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'total_time': total_time, 
        'featured':featured
    }
    return render(request, 'home.html', context)
    # return render(request, 'home.html')


def total_time(request):
    # Current date is hard coded
    latest_entry = Theme.objects.latest("timeStamp")
    date = latest_entry.dropDate
    today = datetime.datetime.now
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    print(countdown_date)

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
    latest_entry = Theme.objects.latest('timeStamp')
    if foo:
        foo = foo.replace('-', ' ')
        try:
            category = Category.objects.get(name=foo)
            products = Product.objects.filter(category=category,  quantity__gt=0)
        except Category.DoesNotExist:
            messages.success(request, ("Category Doesn't Exist!"))
            return redirect('shop')
    else:
        # No category, show all products
        products = Product.objects.filter(quantity__gt=0)
        category = None  # No category selected

    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'products': products, 
        'category': category, 
        'categories': category
    }

    categories = Category.objects.all()  # Pass all categories to the template
    return render(request, 'shop.html', context)

def about(request):
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor
    }
    return render(request, 'about.html', context)

def contact(request):
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor
    }
    return render(request, 'contact.html', context)

# theme HTML - Admin CSS Editor
def edit_theme(request):
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor
    }
    return render(request, 'edit_theme.html', context)

# Request used to update CSS Theme
@csrf_exempt
def submit_theme(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request response"}, status=405)
    try:
        print("Passed thrugh if")
        print(request.POST.get('backgroundColor'))
        dropDate = request.POST.get("dropDate")
        backgroundColor = request.POST.get("backgroundColor")
        bannerImg00 = request.FILES.get("bannerImg00")
        bannerImg01 = request.FILES.get("bannerImg01")
        bannerImg02 = request.FILES.get("bannerImg02")
        fontStyle = request.POST.get("fontStyle")
        dropTitle = request.POST.get("dropTitle")
        fontColor = request.POST.get("fontColor")
        fontWeight = request.POST.get("fontWeight")
        fontBorderThickness = request.POST.get("fontBorderThickness")
        borderColor = request.POST.get("borderColor")

        new_theme = Theme(dropDate = dropDate, 
                          backgroundColor = backgroundColor, 
                          bannerImg00 = bannerImg00, 
                          bannerImg01 = bannerImg01,
                          bannerImg02 = bannerImg02,
                          fontStyle = fontStyle,
                          dropTitle = dropTitle,
                          fontColor = fontColor,
                          fontWeight = fontWeight,
                          fontBorderThickness = fontBorderThickness,
                          borderColor = borderColor)
        
        new_theme.save()
        return JsonResponse({"message": "Theme saved successfully"})
        
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=501)


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

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'cart_items': cart_items,
        'total_price': total_price, 
        'tax_amount': tax_amount, 
        'tax_total': tax_total
    }

    # Render the cart page with items and total and timer count down
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))  # default to 1 if not passed

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
    else:
        session_key = request.session.session_key or request.session.create()
        cart_item, created = Cart.objects.get_or_create(session_key=request.session.session_key, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    cart_items = Cart.objects.filter(customer=customer) if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key)

    return JsonResponse({
        'message': 'Product added to cart successfully!',
        'cart_item_count': sum(item.quantity for item in cart_items),
        'cart_items': [
            {
                "product": {
                    "image_url": item.product.image.url if item.product.image else "",
                    "name": item.product.name,
                    "price": float(item.product.price),
                    "quantity": item.quantity
                }
            }
            for item in cart_items[:4]
        ]
    })

def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_item_id)
        delete_all = request.POST.get("delete_all", "false") == "true"
        quantity_to_remove = int(request.POST.get("quantity", 1))

        # Auth check
        if request.user.is_authenticated:
            if cart_item.customer != request.user.customer:
                return JsonResponse({'message': 'Unauthorized access.'}, status=403)
        else:
            if cart_item.session_key != request.session.session_key:
                return JsonResponse({'message': 'Unauthorized access.'}, status=403)

        # Adjust quantity or delete
        if delete_all:
            cart_item.delete()
        elif cart_item.quantity > quantity_to_remove:
            cart_item.quantity -= quantity_to_remove
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse({'message': 'Item quantity updated or removed.'})
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
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'iframe_code': iframe_code
    }
    return render(request, 'googleCalendar.html', context)

@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'cart_items': cart_items,
        'total_price': total_price, 
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
        return HttpResponse("Failed to create order")

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
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor
    }
    return render(request, 'payment.html', context)

#@authenticated_user
@payment_required
def orderSummary(request, order_id=None):
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        items = OrderItem.objects.filter(order=order)
        pre_tax_total = order.pre_tax_total
        tax_amount = order.tax_amount
        total_amount = order.total_amount
        square_order_id = order.square_order_id  # ✅ Pull it from the order
    else:
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(customer = Customer.objects.filter(user=request.user).first())
        else:
            cart_items = Cart.objects.filter(session_key=request.session.session_key)

        items = cart_items  # So template doesn't break
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'items': items,
        'pre_tax_total': pre_tax_total,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'is_order': bool(order_id),
        'square_order_id': square_order_id  # ✅ Add to context
    }

    return render(request, 'orderSummary.html', context)

# Creating the request for product details
def productDetails(request,pk):
    product = Product.objects.get(id=pk)
    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        'product': product
    }
    return render(request, 'productDetails.html', context)

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

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount

    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        "square_app_id": square_app_id,
        "square_location_id": square_location_id,
        'total_price': total_price,
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

        # **Step 2: Fetch Shipping Rate (if delivery) Add shipping with total**

        # ** Need to actually pass amount through correctly
        cheapest_rate = None
        if delivery_method.lower() == "delivery":
            rates = get_shipping_rates(customerInfo)
            if rates:
                cheapest_rate = get_cheapest_shipping_rate(rates)
                if cheapest_rate:
                    print(total_amount)
                    #total_amount += int(float(cheapest_rate.amount) * 100)  # Convert dollars to cents

                else:
                    return JsonResponse({"status": "error", "message": "Failed to retrieve shipping rates"}, status=400)

        # **Step 3: Process Payment Using Square Order ID**
        payment_request = {
            "source_id": token,
            "idempotency_key": str(uuid.uuid4()),  # Generate unique key
            "amount_money": {
                "amount": total_amount,
                "currency": "USD"
            },
            "autocomplete": True,
            "order_id": square_order_id
        }

        payment_result = client.payments.create_payment(body=payment_request)

        # **Step 4: Payment Successful, Send Confirmation Email**
        if payment_result.is_success():
            square_order_id = payment_result.body['payment']['order_id']  # or wherever the order ID is

            shipping_label_url = None
            tracking_number = None

            customer_obj = customer if request.user.is_authenticated else None
            pre_tax_total = sum(item.product.price * item.quantity for item in cart_queryset)
            tax_amount = float(pre_tax_total) * 0.0725
            total_amount = float(pre_tax_total) + tax_amount

            #Save Order in DB
            order = Order.objects.create(
                customer=customer_obj,
                square_order_id=square_order_id,
                pre_tax_total=pre_tax_total,
                tax_amount=tax_amount,
                total_amount=total_amount,
                delivering=(delivery_method.lower() == "delivery"),
                shipping_label_url=shipping_label_url,
                tracking_number=tracking_number,
            )
            #Update order status
            order.status = "paid"
            order.save()

            #Save each cart item to OrderItem
            for item in cart_queryset:
                product = item.product
                quantity_ordered = item.quantity

                # Update inventory only if enough stock exists
                if product.quantity >= quantity_ordered:
                    product.quantity -= quantity_ordered
                    product.save()

                    # Create the order item with correct quantity
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity_ordered,
                        price_at_purchase=product.price
                    )
                else:
                    # You could raise an error or handle partial inventory here
                    return JsonResponse({
                        "status": "error",
                        "message": f"Insufficient stock for {product.name}."
                    }, status=400)
            #Clear the cart
            cart_queryset.delete()

        # **Step 5: Purchase Shipping Label (Only After Payment)**
            if delivery_method.lower() == "delivery":
                try:
                    if cheapest_rate:
                        transaction = shippo_sdk.transactions.create(
                            components.TransactionCreateRequest(
                                rate=cheapest_rate.object_id,  # Using the rate object_id
                                label_file_type=components.LabelFileTypeEnum.PDF,
                                async_=False
                            )
                        )

                    if transaction.status == "SUCCESS":
                        shipping_label_url = transaction.label_url
                        tracking_number = transaction.tracking_number
                        print(transaction.label_url)
                        print(transaction.tracking_number)
                        #Update order status to shipped
                        order.status = "label created"
                        order.tracking_number = tracking_number
                        order.shipping_label_url = shipping_label_url
                        order.save()

                    else:
                        shipping_label_url = None
                        tracking_number = None
                except Exception as e:
                    shipping_label_url = None
                    tracking_number = None
                    print("Error purchasing shipping label:", str(e))
            else:
                shipping_label_url = None
                tracking_number = None

            email_context = {
                **customerInfo,  # expands: first_name, last_name, email, phone, address
                "delivery_method": delivery_method.lower(),
                "address_details": customerInfo["address"] if delivery_method.lower() == "delivery" else {},
                "order_items": [
                    {
                        "name": item.product.name,
                        "price": item.price_at_purchase,
                        "image_url": item.product.image.url if item.product.image else ""
                    } for item in order.items.all()
                ],
                "total_price": float(order.total_amount),  # or order.total_amount if already Decimal
                "tax_amount": float(order.tax_amount) if hasattr(order, "tax_amount") else 0.00,
                "square_order_id": square_order_id,  # ✅ ADD THIS
                "shipping_cost": float(cheapest_rate.amount) if cheapest_rate else 0.00,
                "shipping_label_url": shipping_label_url,
                "tracking_number": tracking_number,
            }

            # After Square payment is processed(uncomment to make it work)
            email_sent = False
            try:
                send_order_email(email_context)
                email_sent = True
            except Exception as e:
                 print("❌ Email failed to send:", str(e))


            return JsonResponse({"status": "success",
                                "message": "Payment successful!",
                                "redirect_url": reverse("view_order_summary",args=[order.id]),
                                "email_sent": email_sent})

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

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    tax_amount = float(total_price) * 0.0725
    tax_total = float(total_price) + tax_amount

    latest_entry = Theme.objects.latest('timeStamp')
    context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        "square_app_id": square_app_id,
        "square_location_id": square_location_id,
        'total_price': total_price,
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
            latest_entry = Theme.objects.latest('timeStamp')
            context = {
                'dropDate': latest_entry.dropDate,
                'backgroundColor': latest_entry.backgroundColor,
                'bannerImg00': latest_entry.bannerImg00,
                'bannerImg01': latest_entry.bannerImg01,
                'bannerImg02': latest_entry.bannerImg02,
                'fontStyle': latest_entry.fontStyle,
                'dropTitle': latest_entry.dropTitle,
                'fontColor': latest_entry.fontColor,
                'fontWeight': latest_entry.fontWeight,
                'fontBorderThickness': latest_entry.fontBorderThickness,
                'borderColor': latest_entry.borderColor,
                "login_error": "Incorrect email or password"
            }
            return render(request, 'home.html', context)
    else:
        latest_entry = Theme.objects.latest('timeStamp')
        context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor
    }
        return render(request, 'home.html', context)   
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
            latest_entry = Theme.objects.latest('timeStamp')
            context = {
                "signup_errors": errors,
                "signup_data": {
                    "email": request.POST.get("email"),
                    "first_name": request.POST.get("first-name"),
                    "last_name": request.POST.get("last-name"),
                    "phone": request.POST.get("phone"),
                    "text_checkbox": request.POST.get("text-checkbox"),
                    "email_checkbox": request.POST.get("email-checkbox"),
                },
                'dropDate': latest_entry.dropDate,
                'backgroundColor': latest_entry.backgroundColor,
                'bannerImg00': latest_entry.bannerImg00,
                'bannerImg01': latest_entry.bannerImg01,
                'bannerImg02': latest_entry.bannerImg02,
                'fontStyle': latest_entry.fontStyle,
                'dropTitle': latest_entry.dropTitle,
                'fontColor': latest_entry.fontColor,
                'fontWeight': latest_entry.fontWeight,
                'fontBorderThickness': latest_entry.fontBorderThickness,
                'borderColor': latest_entry.borderColor
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
            latest_entry = Theme.objects.latest('timeStamp')
            context = {
                "signup_errors": errors,
                'dropDate': latest_entry.dropDate,
                'backgroundColor': latest_entry.backgroundColor,
                'bannerImg00': latest_entry.bannerImg00,
                'bannerImg01': latest_entry.bannerImg01,
                'bannerImg02': latest_entry.bannerImg02,
                'fontStyle': latest_entry.fontStyle,
                'dropTitle': latest_entry.dropTitle,
                'fontColor': latest_entry.fontColor,
                'fontWeight': latest_entry.fontWeight,
                'fontBorderThickness': latest_entry.fontBorderThickness,
                'borderColor': latest_entry.borderColor
            }   
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


@csrf_exempt
def get_shipping_rates(customerInfo):
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
            name=customerInfo["first_name"] + " " + customerInfo["last_name"],
            street1=customerInfo["address"].get("streetAddress", ""),
            street2=customerInfo["address"].get("addressOptional", ""),
            city=customerInfo["address"].get("city", ""),
            state=customerInfo["address"].get("state", ""),
            zip=customerInfo["address"].get("zipCode", ""),
            country="US",
            phone=customerInfo["phone"],
            email=customerInfo["email"]
        )

        print(f"Address from: {address_from}")
        print(f"Address to: {address_to}")
        # Need to get box dimensions from lily and rough weight
        parcel = components.ParcelCreateRequest(
            length="5",
            width="5",
            height="5",
            distance_unit=components.DistanceUnitEnum.IN,
            weight="2",
            mass_unit=components.WeightUnitEnum.LB
        )

        shipment = shippo_sdk.shipments.create(
            components.ShipmentCreateRequest(
                address_from=address_from,
                address_to=address_to,
                parcels=[parcel],
                async_=False
            )
        )
        if shipment.status == "SUCCESS":
                # Retrieve and return the list of rates
                return shipment.rates
        else:
                print(f"Error fetching shipping rates: {shipment.messages}")
                return None

def get_cheapest_shipping_rate(rates):
    """Find the cheapest shipping rate from available rates."""
    if rates:
        return min(rates, key=lambda x: float(x.amount))  # Returns cheapest rate object
        print(f"Cost: {cheapest_rate.amount} {cheapest_rate.currency}")
    return None

@register.inclusion_tag('orderCartSummary.html', takes_context=True)
def orderCartSummary(context):
    return {
        'orderCartSummary': context['data'],
    }


def subscribe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            

            if not email and not phone:
                return JsonResponse({"success": False, "message": "Please provide an email or phone number."}, status=400)

            # ✅ Email format validation FIRST
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    return JsonResponse({"success": False, "message": "Invalid email format."}, status=400)

            # ✅ Phone format validation (optional)
            if phone and not re.match(r'^\d{10}$', phone):
                return JsonResponse({"success": False, "message": "Phone number must be 10 digits."}, status=400)

            # ✅ Now check if already subscribed
            if email and Subscriber.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "Email is already subscribed."})
            if phone and Subscriber.objects.filter(phone=phone).exists():
                return JsonResponse({"success": False, "message": "Phone number is already subscribed."})

            # ✅ Save
            Subscriber.objects.create(email=email or None, phone=phone or None)


            # Only send welcome email if they signed up with an email
            if email:
                html_content = render_to_string("subscription.html", {"email": email})
                text_content = strip_tags(html_content)

                email_message = EmailMultiAlternatives(
                    subject="🎉 Welcome to MoonWalk Threads!",
                    body=text_content,
                    from_email="projectmoonwalk01@gmail.com",
                    to=[email],
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send()

            return JsonResponse({"success": True, "message": "Subscription successful."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid data format."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def unsubscribe(request, token):
    subscriber = get_object_or_404(Subscriber, unsubscribe_token=token)
    subscriber.delete()
    return render(request, "unsubscribe.html", {"email": subscriber.email})

def send_order_email(context):
    try:
        html_content = render_to_string("order_confirmation_email.html", context)
        text_content = strip_tags(html_content)
        subject = f"Order #{context['square_order_id']}"
        from_email = "projectmoonwalk01@gmail.com"
        recipient_list = [context["email"]]

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print("Email Error:", e)
        return False

@login_required
def profile(request):
    user = request.user

    customer = getattr(request.user, "customer", None)
    print(f"DEBUG: Logged-in user's email: {request.user.email}")
    if customer:
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        address = customer.street_address
    else:
        # Hardcoded data for non-logged-in users
        orders = []
        address = "No address available"
        user_data = {
            "email": user.email,
            "password": "********",
            "address": address,
            "orders": orders
        }
        latest_entry = Theme.objects.latest('timeStamp')
        context = {
        'dropDate': latest_entry.dropDate,
        'backgroundColor': latest_entry.backgroundColor,
        'bannerImg00': latest_entry.bannerImg00,
        'bannerImg01': latest_entry.bannerImg01,
        'bannerImg02': latest_entry.bannerImg02,
        'fontStyle': latest_entry.fontStyle,
        'dropTitle': latest_entry.dropTitle,
        'fontColor': latest_entry.fontColor,
        'fontWeight': latest_entry.fontWeight,
        'fontBorderThickness': latest_entry.fontBorderThickness,
        'borderColor': latest_entry.borderColor,
        "user_data": user_data
        }   
        return render(request, "profile.html", context)


@require_POST
@login_required
def update_address(request):
    customer = getattr(request.user, "customer", None)
    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect("profile")

    street = request.POST.get("street_address", "").strip()
    street2 = request.POST.get("street_address2", "").strip()
    city = request.POST.get("city", "").strip()
    state = request.POST.get("state", "").strip()
    zip_code = request.POST.get("zip_code", "").strip()

    if not street or not city or not state or not zip_code:
        messages.error(request, "All required address fields must be filled.")
        return redirect("profile")

    # Save the updated values
    customer.street_address = street
    customer.street_address2 = street2
    customer.city = city
    customer.state = state
    customer.zip_code = zip_code
    customer.save()

    messages.success(request, "Your address has been updated.")
    return redirect("profile")


