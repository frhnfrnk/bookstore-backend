from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.customer_list, name='customer_list'),
]