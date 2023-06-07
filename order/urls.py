from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.order_list, name='order_list'),
    path('history/', api.history_list, name='order_history'),
]