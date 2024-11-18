from django.shortcuts import render
import datetime
from .models import Product
from .square_service import client
from django.http import JsonResponse
import json
import uuid

def home(request):
    # Current date is hard coded
    date = "2024-12-06 00:00:00"
    today = datetime.datetime.now()
    # Specify the date format being provided
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Calculate the time to the specified date from when the web is loaded
    total_time = countdown_date - today
    # Convert the total time to seconds
    total_time = total_time.total_seconds()
    products = Product.objects.all()
    return render(request, 'home.html', {'total_time': total_time, 'products':products})
    # return render(request, 'home.html')

def total_time(request):
    # Current date is hard coded
    date = "2024-12-06 00:00:00"
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
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def cart(request):
    #mock items
    cart_items = [
        {'name': 'Item 1', 'price': 79.99,'size': 'M', 'image': 'photos/Itemimage1.png'},
        {'name': 'Item 2', 'price': 12.99,'size': 'M', 'image': 'photos/Itemimage2.png'},
        {'name': 'Item 3', 'price': 45.99,'size': 'M','image': 'photos/Itemimage3.png'},
        {'name': 'Item 4', 'price': 25.99,'size': 'M', 'image': 'photos/Itemimage4.png'},
        {'name': 'Item 5', 'price': 8.99, 'size': 'M','image': 'photos/Itemimage1.png'}
    ]
    
    # Calculate total price of items in the cart
    cart_total = sum(item['price'] for item in cart_items)
    cart_total = f"{cart_total:.3f}"
    # Render the cart page with items and total
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def googleCalendar(request):
    iframe_code = '''
    <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FLos_Angeles&showPrint=0&showTz=0&showTabs=0&showTitle=0&src=YzI0ZTliYzcwNDhkMzg0NDczMmM2NTY5NzljODY4MDgzNjZlOWI1MGVhZGM2ZmUxNTBjODY2OWE3YTYxMjRkMUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23B39DDB" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>
    '''
    return render(request, 'googleCalendar.html', {'iframe_code': iframe_code})

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


def paymentPortal(request):
    square_app_id = 'sandbox-sq0idb-8IPgsCCDGo1xxuoCMh0SSQ'
    square_location_id = 'LNG128XEAPR21'
    context = {
        "square_app_id": square_app_id,
        "square_location_id": square_location_id
    }
    return render(request, 'paymentPortal.html', context)

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