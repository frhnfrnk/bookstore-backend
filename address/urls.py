from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.address_list, name='address_list'),
    path('<int:pk>/', api.address_detail, name='address_detail')
]