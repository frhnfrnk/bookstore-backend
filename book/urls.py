from django.urls import path

from . import api
from . import api2


# path "book/"
urlpatterns = [
    path('', api.book_list_create, name='book_list_create'),
    path('<int:pk>/', api.book_detail_update_delete, name='book_detail_update_delete'),
    path('search/<str:search>/', api.book_search, name='book_search'),
    path('category/', api2.category_list, name='category_list'),
    path('category/<int:pk>/', api2.book_category_list, name='book_category_list'),
    path('publisher/', api2.publisher_list, name='publisher_list'),
    path('publisher/<int:pk>/', api2.book_publisher_list, name='book_publisher_list'),
    path('language/', api2.language_list, name='language_list'),
    path('language/<int:pk>/', api2.book_language_list, name='book_language_list'),
    path('author/', api2.author_list, name='author_list'),
    path('author/<int:pk>/', api2.book_author_list, name='book_author_list'),
]