from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

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
