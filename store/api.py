from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Store

from .serializers import StoreSerializer

@api_view(['GET'])
def store_list(request):
    stores = Store.objects.all()

    serializer = StoreSerializer(stores, many=True)

    return JsonResponse(serializer.data, safe=False)