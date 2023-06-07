from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Address

from .serializers import AddressSerializer

@api_view(['GET'])
def address_list(request):
    address_list = Address.objects.all()

    serializer = AddressSerializer(address_list, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def address_detail(request, pk):
    address = Address.objects.get(pk=pk)

    serializer = AddressSerializer(address, many=False)

    return JsonResponse(serializer.data, safe=False)