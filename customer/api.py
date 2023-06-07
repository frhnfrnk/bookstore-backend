from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Customer

from .serializers import CustomerSerializer

@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all()

    serializer = CustomerSerializer(customers, many=True)

    return JsonResponse(serializer.data, safe=False)