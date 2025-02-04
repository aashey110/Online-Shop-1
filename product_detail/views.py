from django.shortcuts import render

from shop.models import Product

# Create your views here.
def product_detail(request, id):
    product = Product.objects.get(id=id)
    data = {
        'product': product,
    }
    return render(request, 'product_detail.html', data)