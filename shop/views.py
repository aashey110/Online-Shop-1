from django.shortcuts import render

from .models import Product

# Create your views here.
def shop(request):
    sort_option = request.GET.get('sort', 'price-asc')  # Default to 'price-asc'

    if sort_option == 'price-asc':
        products = Product.objects.all().order_by('price')
    elif sort_option == 'price-desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()
    return render(request, 'shop.html', {'products': products, 'sort_option': sort_option})