from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Order, OrderItem
from .forms import ProfileForm, ContactForm, PaymentForm
from .models import Profile, OrderPayment, Contact
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import JsonResponse

User = get_user_model()


def home(request):
    products = Product.objects.filter(available=True)[:12]
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    # If this is an AJAX request, return JSON so front-end can stay on the page
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        cart_count = sum(i.quantity for i in cart.items.all())
        return JsonResponse({'success': True, 'cart_count': cart_count})
    return redirect('home')


@login_required
def remove_from_cart(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if request.method == 'POST':
        item.delete()
    return redirect('view_cart')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            auth_login(request, user)
            # create an empty cart
            Cart.objects.get_or_create(user=user)
            messages.success(request, 'Account created and you are now logged in')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.exists():
        return redirect('home')
    if request.method == 'POST':
        pform = PaymentForm(request.POST)
        if pform.is_valid():
            order = Order.objects.create(user=request.user, total=cart.total)
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            payment = pform.save(commit=False)
            payment.order = order
            payment.save()
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully')
            return render(request, 'store/checkout_done.html', {'order': order})
    else:
        pform = PaymentForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'form': pform})


@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            # If a full_name was provided and welcome_text is empty or default, set a friendly welcome
            if p.full_name:
                # extract first name
                first = p.full_name.split()[0]
                if not p.welcome_text or 'Welcome' in p.welcome_text:
                    p.welcome_text = f"Welcome, {first}!"
            p.save()
            messages.success(request, 'Profile updated')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/dashboard.html', {'form': form, 'profile': profile})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})
from django.shortcuts import render

# Create your views here.
