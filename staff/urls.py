from django.urls import path

from . import api


# path "book/"
urlpatterns = [
    path('', api.staff_list, name='staff_list'),
    path('signup/', api.signup, name='signup'),
    path('login/', api.login, name='login'),
    path('logout/', api.logout, name='logout'),
    path('delete/<int:staff_id>/', api.delete_staff, name='delete_staff')
]