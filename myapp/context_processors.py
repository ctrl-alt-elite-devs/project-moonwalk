from myapp.models import Cart
from django.conf import settings


def cart_context(request):
    cart_items = []
    cart_item_count = 0
    total_price = 0

    if request.path.startswith("/admin/"):
        return {}  # ✅ Prevent errors in Django Admin

    if request.user.is_authenticated:
        customer = getattr(request.user, "customer", None)  # ✅ Use customer instead of user
        if customer:
            cart_items = Cart.objects.filter(customer=customer)
    else:
        session_key = request.session.session_key
        if session_key:
            cart_items = Cart.objects.filter(session_key=session_key)

    cart_item_count = len(cart_items)
    total_price = sum(item.product.price for item in cart_items)

    return {
        "cart_items": cart_items,
        "cart_item_count": cart_item_count,
        "total_price": total_price,
    }

def google_client_id(request):
    return {
        'google_client_id': settings.OAUTH_GOOGLE_CLIENT_ID
    }