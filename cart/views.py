from django.shortcuts import render, redirect
from .models import Product, Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    # Calculate the overall total price for all items
    total_price = sum(item.total_price for item in cart_items)
    data = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', data)


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity},
    )

    if not created:
        # If the product is already in the cart, update the quantity
        cart_item.quantity += quantity
        cart_item.save()

    # Show a success message
    messages.success(request, 'Added to cart successfully')

    return redirect('product_detail', id=id)  # Redirect to the product detail page