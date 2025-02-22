from myapp.models import Cart, Customer

def cart_context(request):
    cart_items = []
    cart_item_count = 0
    total_price = 0

    if request.user.is_authenticated:
        # Safely get the customer object
        customer = getattr(request.user, "customer", None)

        if customer:
            cart_items = Cart.objects.filter(customer=customer)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()  # Ensure session exists
            session_key = request.session.session_key

        cart_items = Cart.objects.filter(session_key=session_key)

    # Update cart item count and total price
    cart_item_count = len(cart_items)  # Get the number of unique cart items
    total_price = sum(item.product.price for item in cart_items)

    return {
        "cart_items": cart_items,
        "cart_item_count": cart_item_count,
        "total_price": total_price,
    }