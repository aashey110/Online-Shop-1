from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart')
]
