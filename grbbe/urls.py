from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import api

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('table/', api.table, name='table'),
    path('api/book/', include('book.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/order/', include('order.urls')),
    path('api/staff/', include('staff.urls')),
    path('api/store/', include('store.urls')),
    path('api/address/', include('address.urls')),
]
