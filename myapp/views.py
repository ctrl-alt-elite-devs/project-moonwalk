from django.shortcuts import render
import datetime
from .models import Cart, Product
from .square_service import client
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
    return render(request, 'home.html', 'cart.html', context)

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
    <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FLos_Angeles&showPrint=0&showTz=0&showTabs=0&showTitle=0&src=YzI0ZTliYzcwNDhkMzg0NDczMmM2NTY5NzljODY4MDgzNjZlOWI1MGVhZGM2ZmUxNTBjODY2OWE3YTYxMjRkMUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23B39DDB" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>
    '''
    return render(request, 'googleCalendar.html', {'iframe_code': iframe_code})

def checkout(request):
    return render(request, 'checkout.html')

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


