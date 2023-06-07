from rest_framework import serializers

from .models import Store, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):

    address = AddressSerializer()
    class Meta:
        model = Store
        fields = '__all__'

