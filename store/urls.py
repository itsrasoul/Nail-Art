from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
