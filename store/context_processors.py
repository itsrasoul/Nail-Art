from .models import Cart

def cart_and_profile(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(item.quantity for item in cart.items.all())
    except Exception:
        cart_count = 0
    return {
        'cart_count': cart_count,
    }
