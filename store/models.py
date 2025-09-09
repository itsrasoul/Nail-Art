from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    welcome_text = models.CharField(max_length=200, blank=True, default='Welcome to Nail Blossom')

    def __str__(self):
        return f"Profile: {self.user.username}"


class OrderPayment(models.Model):
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('cashapp', 'Cash App'),
        ('crypto', 'Cryptocurrency'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    card_name = models.CharField(max_length=200, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    paypal_email = models.EmailField(blank=True)
    cashapp_tag = models.CharField(max_length=100, blank=True)
    crypto_address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} ({self.method})"


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name}"
