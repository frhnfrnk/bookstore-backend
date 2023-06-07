from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.cart_list, name='cart_list'),
    path('add/', api.add_to_cart, name='add_to_cart'),
]