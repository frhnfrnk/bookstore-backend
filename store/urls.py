from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.store_list, name='store_list'),
]