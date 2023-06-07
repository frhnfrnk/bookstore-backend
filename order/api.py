from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Order

from .serializers import OrderSerializer

@api_view(['GET'])
def order_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM "order"')
        rows = cursor.fetchall()
    
    orders = []
    for row in rows:
        order = {
            'order_id': row[0],
            'inventory': row[1],
            'staff': row[2],
            'customer': row[3],
            'order_date': row[4],
        }
        orders.append(order)
    
    return JsonResponse(orders, safe=False)

@api_view(['GET'])
def history_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM order_history')
        rows = cursor.fetchall()

    histories = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM "order" WHERE order_id = %s', [row[0]])
            order_row = cursor.fetchone()

        history = {
            'history_id': row[0],
            'order_id': order_row[0],
            'staff': order_row[2],
            'customer': order_row[3],
            'order_date': order_row[4],
        }
        histories.append(history)

    return JsonResponse(histories, safe=False)
