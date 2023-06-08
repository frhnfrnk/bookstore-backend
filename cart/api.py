from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from .models import Cart


@api_view(['GET'])
def cart_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Cart')
        rows = cursor.fetchall()

    carts = []
    for row in rows:
        cart = {
            'cart_id': row[0],
            'book_id': row[1],
            'staff_id': row[2]
        }
        carts.append(cart)
    
    return JsonResponse(carts, safe=False)

@api_view(['POST'])
def add_to_cart(request):
    book_id = request.data['book_id']
    staff_id = request.data['staff_id']

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Cart (book_id, staff_id) VALUES (%s, %s)', [book_id, staff_id])
    
    return JsonResponse({'message': 'success'})
